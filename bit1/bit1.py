from collections import Sequence
from magma import *
from magma.bitutils import clog2
from mantle import LUT6, I4, I5, FF, Mux2, Mux4, Mux8, Mux16

from .asm import assemble, disassemble
from .ROMN import ROM

MAXLOGN  = 5
MAXLOGNI = 4
MAXLOGNO = 5

# Instruction memory for inputs and outputs.
#
#  The number of input bits is equal to ni. 
#
#  The number of output bits is equal to no.
#
def Inst(mem, ni, no, ff=False, has_ce=False, has_reset=False):
    return ROM(mem, ni, no, ff, has_ce=has_ce, has_reset=has_reset)

#
# Sequencer
#
#  The program counter pc is logn bits wide.
#
#  The output of the circuit contains logn bits which is the
#  the next pc.
#
#  The input to the sequencer is a single bit I.
#
#  The sequencer constains two pc pc0 and pc1. The input I controls
#  whether the output is pc0 or pc1. Thus, the sequencer ROM input is
#  logn+1 bits wide.
#

def DefineSeq(mem, logn, has_ce=False, has_reset=False):
    assert logn == 5 or logn == 6
    assert len(mem[0]) == logn
    class _Seq(Circuit):
        name = f'Seq{logn}'
        IO = ['I', In(Bit), 'O', Out(Bits(logn))] \
                + ClockInterface(has_ce=has_ce, has_reset=has_reset)
        @classmethod
        def definition(io):
            pc = ROM(mem, logn+1, logn, 
                     ff=True, has_ce=has_ce, has_reset=has_reset)
            wire( pc( concat(pc.O, bits([io.I])) ), io.O )
            wireclock(io, pc)
    return _Seq

def Seq(mem, logn, has_ce=False, has_reset=False):
    return DefineSeq(mem, logn, has_ce=has_ce, has_reset=has_reset)()

#
# Return a MUX for the input.
#
#  The number of inputs ni is given by log of the number of actual inputs.
#
#  Allowed values are [1, 2, 3, 4] which corresponds to a maximum number
#  of inputs of [2, 4, 8, 16]
#
def Mux(logni):
    assert 1 <= logni <= 4

    if   logni == 1:
        return Mux2()
    elif logni == 2:
        return Mux4()
    elif logni == 3:
        return Mux8()
    elif logni == 4:
        return Mux16()

# setup input datapath
def DefineInput(data, LOGN, LOGNI):
    assert 1 <= LOGNI <= 4
    NI = 1 << LOGNI
    class _Input(Circuit):
        name = f'Input{LOGN}_{NI}'
        IO = ['pc', In(Bits(LOGN)), 'I', In(Bits(NI)), 'O', Out(Bit)]
        @classmethod
        def definition(io):
            inst = Inst(data, LOGN, LOGNI)
            mux = Mux(LOGNI)
            if NI == 2:
                wire(mux(io.I, inst(io.pc)[0]), io.O)
            else:
                wire(mux(io.I, inst(io.pc)), io.O)
    return _Input

def Input(data, logn, logni):
    return DefineInput(data, logn, logni)()

def ADDR(a, n):
    m = 64 // n
    res = 0
    for i in range(m):
        res |= a << n * i
    return res

# DecodedOutputRegister creates a decoded output register.
#
#  The number of decoded outputs is no. The number of bits input to the
#  decoder is logno.  no must be less than (1<<logno).
# 
def DecodedOutputRegister(logno, no, has_ce, has_reset, init):

    assert 1 <= logno <= 4
    assert no <= 1 << logno

    def out1(y):

        a = ADDR(1 << y, 1 << logno)
        a_n = ~a

        # The output is fed back to the input. If the output is not decoded,
        # then the output is unchanged. That is, the output of this circuit
        # is the current outout (I5), otherwise the output is equal to I4.
        # ROM3
        lut = uncurry(LUT6((a & I4) | (a_n & I5)))
        reg = FF(init, has_ce=has_ce, has_reset=has_reset)

        reg(lut.O)

        I = lut.I
        # wire the reg to I5. 
        wire(reg.O, I[5])
        if logno < 2: wire(0, I[1])
        if logno < 3: wire(0, I[2])
        if logno < 4: wire(0, I[3])

        args = ["I0", I[0:logno], 
                "I1", I[4],
                "O", reg.O] + reg.clockargs()
        return AnonymousCircuit(args)

    return fork(col(out1, no))

def DefineDecodedOutput(mem, LOGN, LOGNO, NO, has_ce=False, has_reset=False, init=0):

    class _Output(Circuit):
        name = f'DecodedOutput{NO}{"_ce" if has_ce else ""}{"_r" if has_reset else ""}'
        IO = ['pc', In(Bits(LOGN)), 'O', Out(Bits(NO))] \
                + ClockInterface(has_ce, has_reset)
        @classmethod
        def definition(io):
            # LOGNO+1 : LOGNO bits for decoader, 1 bit for value
            inst = Inst(mem, LOGN, LOGNO)
            O = inst(io.pc)
            out = DecodedOutputRegister(LOGNO-1, NO, has_ce, has_reset, init)
            wire( out(O[0:LOGNO-1], O[LOGNO-1]), io.O )
            wireclock(io, out)

    return _Output


def DecodedOutput(mem, logn, logno, no, has_ce=False, has_reset=False, init=0):
     return DefineDecodedOutput(mem, logn, logno, no, 
                           has_ce=has_ce, has_reset=has_reset, init=init)()

def DefineOutput(mem, LOGN, LOGNO, has_ce=False, has_reset=False, init=0):

    class _Output(Circuit):
        name = f'Output{LOGNO}{"_ce" if has_ce else ""}{"_r" if has_reset else ""}'
        IO = ['pc', In(Bits(LOGN)), 'O', Out(Bits(LOGNO))] \
                + ClockInterface(has_ce, has_reset)
        @classmethod
        def definition(io):
            inst = Inst(mem, LOGN, LOGNO, has_ce, has_reset, init)
            wire( inst(io.pc), io.O )
            wireclock(io, inst)

    return _Output


def Output(mem, logn, logno, has_ce=False, has_reset=False, init=0):
     return DefineOutput(mem, logn, logno,
                           has_ce=has_ce, has_reset=has_reset, init=init)()

#    #if output == 'parallel':
#        print( 'creating parallel output' )
#        inst = Inst(dout, LOGN, LOGNO,
#                  output==output,
#                  has_ce=has_ce, has_reset=has_reset)
#        return inst, None, inst(pc)
# determine number of inputs and number of outputs
def configure(n, ni, no, output):

    logn = clog2(n)
    assert logn <= MAXLOGN

    logni = clog2(ni)
    assert logni <= MAXLOGNI

    if output == 'decoded':
        if no == 1:
            no = 2
        logno = clog2(no) + 1 # 1 extra bit for output value
    else:
        logno = no
    assert logno <= MAXLOGNO

    return logn, logni, logno


def DefineBit1(main, N, NI, NO, mode='decoded', 
                has_ce=False, has_reset=False, init=0, debug=False):

    assert NI > 0
    assert NO > 0
    LOGN, LOGNI, LOGNO = configure(N, NI, NO, mode)

    print( 'Building 1-bit computer' )
    print( 'instructions: %d (%d bits)' % (N, LOGN) )
    print( 'inputs: %d (%d bits)' % (NI, LOGNI) )
    print( 'outputs: %d (%d bits)' % (NO, LOGNO) )

    mem, controlflow, datain, dataout = assemble(main, LOGN, LOGNI, LOGNO)
    if( debug ):
        disassemble(mem)

    assert len(controlflow[0]) == LOGN

    class _Bit1(Circuit):
        name = f'Bit1_{N}_{NI}_{NO}{"_ce" if has_ce else ""}{"_r" if has_reset else ""}'
        IO = ['I', In(Bits(NI)), "O", Out(Bits(NO))] + \
                ClockInterface(has_ce=has_ce, has_reset=has_reset)

        @classmethod
        def definition(io):
            # create sequencer
            seq = Seq(controlflow, LOGN, has_ce, has_reset)

            # create input ports
            if NI == 1:
                wire( io.I[0], seq.I )
            else:
                input = Input(datain, LOGN, LOGNI)
                if NI < 1<<LOGNI:
                    I = concat(io.I, bits(0,(1<<LOGNI)-NI)) 
                else:
                    I = io.I
                wire( input( seq.O, I ), seq.I )

            # create ouput ports
            if mode == 'decoded':
                output = DecodedOutput(dataout, LOGN, LOGNO, NO, has_ce, has_reset, init)
            else:
                output = Output(dataout, LOGN, LOGNO, has_ce, has_reset, init)

            wire( output( seq.O )[:NO], io.O )

            wireclock(io, seq)
            wireclock(io, output)

    return _Bit1

def Bit1(main, n, ni, no, 
            mode='decoded', 
            has_ce=False, has_reset=False, init=0,
            debug=False):
    return  DefineBit1(main, n, ni, no, 
                mode=mode,
                has_ce=has_ce, has_reset=has_reset, init=0, debug=debug)()

