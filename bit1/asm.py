import inspect
from magma import *
from magma.bitutils import int2seq

LOGN = 5
N = 1 << LOGN

LOGNI = 2
NI = 1 << LOGNI

LOGNO = 4
NO = 4

RNULL = 0


_mem = 0
_pc = 0

labels = {}
_pass = 0

mode = 0

def org(newpc):
    global _pc
    _pc = newpc

def equ(name, value):
    global labels
    labels[name] = value

def label(name=None):
    global labels, _pass
    if name: 
        if _pass == 0:
            labels[name] = _pc
        if _pass == 1:
            return labels[name]
        return 0
    return _pc

def inst( o, i=None, next_pc0=None, next_pc1=None, **kwargs):

    if mode:
        if o == None:
            oaddr = RNULL
            odata = 0
        else:
            oaddr = o[0]
            odata = o[1]
        assert 0 <= oaddr < (1 << LOGNO-1)
        assert odata == 0 or odata == 1
        o = int2seq(oaddr | odata << LOGNO-1, LOGNO)
    else:
        assert o != None

    jump = kwargs.get('jump', None)
    skip = kwargs.get('skip', None)

    if i is None:
        i = 0
        next_pc0 = None
        next_pc1 = None

    assert i >= 0 and i < (1 << LOGNI)
    i = int2seq(i, LOGNI) if LOGNI > 0 else [0]

    global _pc, _mem

    if next_pc0 is None:
        if   jump is not None: next_pc0 = jump
        elif skip is not None: next_pc0 = _pc + skip + 1
        else: next_pc0 = _pc+1

    if next_pc1 is None:
        if   jump is not None: next_pc1 = jump
        elif skip is not None: next_pc1 = _pc + skip + 1
        else: next_pc1 = _pc+1

    assert next_pc0 >= 0 and next_pc0 < N
    assert next_pc1 >= 0 and next_pc1 < N

    next_pc0 = int2seq(next_pc0, LOGN)
    next_pc1 = int2seq(next_pc1, LOGN)


    assert _pc < N

    _mem[_pc] = [ o, i, next_pc0, next_pc1 ]
    _pc = _pc + 1



def jump( pc ):
    inst( None, 0, jump=pc )

def halt():
    jump( _pc )


def if0( port, pc ):
    inst( None, port, next_pc0=pc )

def if1( port, pc ):
    inst( None, port, next_pc1=pc )

def ifelse( port, next_pc1, next_pc0 ):
    inst( None, port, next_pc0=next_pc0, next_pc1=next_pc1 )


def skipif1( port, n=1 ):
    inst( None, port, next_pc1=_pc+n+1, next_pc0=_pc+1)

def skipif0( port, n=1 ):
    inst( None, port, next_pc0=_pc+n+1, next_pc1=_pc+1 )

def skip( n=1 ):
    inst( None, port, skip=n )

def pause( port ):
    inst( None, port, next_pc0=_pc, next_pc1=_pc+1 )

def sob(tick,test):
    set(tick)
    inst( [tick,0], test,0 )

def out( *args, **kwargs):
    inst( list(args), **kwargs )

def set( port, **kwargs ):
    if mode:
        out( port, 1, **kwargs )
    else:
        o = NO * [1]
        out( *o, **kwargs )

def clr( port, **kwargs ):
    if mode:
        out( port, 0, **kwargs )
    else:
        o = NO * [0]
        out( *o, **kwargs )


def nop():
    inst( None )

def delay(n):
    for i in range(n):
        nop()


def mov( ra, rb ):
    skipif1( ra )
    out( rb, 0, skip=1 )
    out( rb, 1 )

def not_( ra, rb ):
    skipif0( ra )
    out( rb, 0, skip=1 )
    out( rb, 1 )

def and_( ra, rb, rc ):
    skipif0( ra, 2 )
    skipif0( rb, 1 )
    out( rc, 1, skip=1 )
    out( rc, 0 )

def or_( ra, rb, rc ):
    skipif1( ra, 2 )
    skipif1( rb, 1 )
    out( rc, 0, skip=1 )
    out( rc, 1 )

def xor( ra, rb, rc ):
    skipif1( ra, 1 )
    ifelse( rb, _pc+2, _pc+3 ) # ra=0
    ifelse( rb, _pc+2, _pc+1 ) # ra=1
    out( rc, 1, skip=1 ) # ra != rb
    out( rc, 0 )         # ra == rb


def val(bits):
    val = 0
    n = len(bits)
    for i in range(n):
        if bits[i]: val |= (1 << i)
    return val

def init(logn, logni, logno, o='decoded'):

    global LOGN, N
    LOGN = logn
    N = 1 << LOGN

    global LOGNI, NI
    LOGNI = logni
    NI = 1 << LOGNI

    global LOGNO, NO
    LOGNO = logno
    NO = 1 << (LOGNO-1) if o == 'decoded' else LOGNO

    global RNULL
    RNULL = NO-1

    global labels
    labels = {}

    global mode
    mode = o == 'decoded'

    global _mem
    _mem = N * [0]
    for i in range(N):
        if mode:
            inst( None, jump=0 )
        else:
            inst( NO * [0], jump=0 )

    g = {}

    for i in range(NI):
        g['I' + str(i)] = i

    for i in range(NO):
        g['O' + str(i)] = i

    g['NI'] = NI
    g['NO'] = NO

    g['label'] = label
    g['org'] = org

    g['inst'] = inst

    g['out'] = out
    g['set'] = set
    g['clr'] = clr

    g['skipif0'] = skipif0
    g['skipif1'] = skipif1
    g['skip'] = skip

    g['if0'] = if0
    g['if1'] = if1
    g['ifelse'] = ifelse

    g['pause'] = pause

    g['jump'] = jump
    g['halt'] = halt

    g['sob'] = sob


    g['nop'] = nop
    g['delay'] = delay

    g['mov'] = mov
    g['not_'] = not_

    g['and_'] = and_
    g['or_'] = or_
    g['xor'] = xor

    return g

def assemble(main, logn, logni, logno, mode='decoded'):

    g = init(logn, logni, logno, mode)

    global _mem, _pc, _pass

    _pc = 0
    _pass = 0
    exec( inspect.getsource( main ), g )

    _pc = 0
    _pass = 1
    exec( inspect.getsource( main ), g )

    #dout, din, pc0, pc1 = _mem[0]
    #print( 'len(dout) =', len(dout) )
    #print( 'len(din) =', len(din) )
    #print( 'len(pc0) =', len(pc0) )
    #print( 'len(pc0) =', len(pc1) )

    din, dout, pc0, pc1 = N*[0], N*[0], N*[0], N*[0]
    for i in range(N):
        dout[i], din[i], pc0[i], pc1[i] = _mem[i]
    seq = pc0 + pc1

    return _mem, seq, din, dout

def disassemble(mem):
    fmt = "%02X"
    for pc in range(N):
        m = mem[pc]
        print(fmt % pc, end=': ')

        o = m[0]
        i = val(m[1])
        pc0 = val(m[2])
        pc1 = val(m[3])

        if mode:
            n = len(o)
            p = val(o[:n-1])
            if p < 1<<LOGNO:
                print( f'out(%d,%d)' % (p,o[n-1]), end=' ')
            else:
                if pc0 == pc1 and pc0 == pc+1:
                    print ('nop()', end=' ')
        else:
            print( 'out(', o, ')', end=' ')

        if pc0 == pc1:
            if pc0 != pc+1:
                print( 'jump(%s)' % (fmt % pc0), end=' ')
        else:
            print( 'ifelse(%d,%s,%s)' % (i, fmt % pc0, fmt % pc1), end=' ')

        print()

