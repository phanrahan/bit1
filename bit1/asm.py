import logging
from magma.bitutils import int2seq

__all__ = ['assemble', 'disassemble', 'org', 'equ', 'label']


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

decoded = 0

def getpc(n=0):
    global _pc
    return (_pc+n)%N

def setpc(pc):
    global _pc
    if not (0 <= pc < N):
        logging.warning(f"pc: {pc} not in range({N})")
        pc %= N
    _pc = pc

def org(newpc):
    setpc(newpc)

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

    global _pc, _mem

    #if _pass == 1:
    #    print(_pc, 'inst',o,i,next_pc0,next_pc1)
    #    print('mem[0]=',_mem[0])
    if decoded:
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

    assert 0 <= i < NI
    i = int2seq(i, LOGNI) if LOGNI > 0 else [0]


    if next_pc0 is None:
        if   jump is not None: next_pc0 = jump
        elif skip is not None: next_pc0 = (_pc + skip + 1)%N
        else: next_pc0 = (_pc+1)%N

    if next_pc1 is None:
        if   jump is not None: next_pc1 = jump
        elif skip is not None: next_pc1 = (_pc + skip + 1)%N
        else: next_pc1 = (_pc+1)%N

    assert 0 <= next_pc0 < N
    assert 0 <= next_pc1 < N

    #if _pass == 1:
    #    print('fullinst',o,i,next_pc0,next_pc1)
    next_pc0 = int2seq(next_pc0, LOGN)
    next_pc1 = int2seq(next_pc1, LOGN)


    assert _pc < N

    _mem[_pc] = [ o, i, next_pc0, next_pc1 ]
    setpc((_pc+1)%N)

    #if _pass == 1:
    #    print('mem[0]=',_mem[0])



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

    global decoded
    decoded = (o == 'decoded')

    global _mem
    _mem = N * [0]
    for i in range(N):
        if decoded:
            inst( None, jump=0 )
        else:
            inst( NO * [0], jump=0 )

def assemble(prog, logn, logni, logno, mode='decoded'):

    init(logn, logni, logno, mode)

    global _mem, _pc, _pass

    _pc = 0
    _pass = 0
    prog()

    _pc = 0
    _pass = 1
    prog()

    din, dout, pc0, pc1 = N*[0], N*[0], N*[0], N*[0]
    for i in range(N):
        dout[i], din[i], pc0[i], pc1[i] = _mem[i]
    seq = pc0 + pc1

    return _mem, seq, din, dout

def val(bits):
    val = 0
    n = len(bits)
    for i in range(n):
        if bits[i]: val |= (1 << i)
    return val

def disassemble(mem):
    fmt = "%X"
    for pc in range(N):
        m = mem[pc]
        print("%02X" % pc, end=': ')

        o = m[0]
        i = val(m[1])
        pc0 = val(m[2])
        pc1 = val(m[3])
        #print(o,i,m[2],pc0,m[3],pc1)

        if decoded:
            n = len(o)
            p = val(o[:n-1])
            if p < 1<<LOGNO:
                if p != RNULL:
                    print( f'out(port=%d,value=%d)' % (p,o[n-1]), end=' ')
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

