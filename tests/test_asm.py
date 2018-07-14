from magma.bitutils import clog2
from bit1.asm import assemble, disassemble, compile

N = 32
LOGN = clog2(N)

NI = 2
LOGNI = clog2(NI)

NO = 2
LOGNO = clog2(NO) + 1

def prog():
    and_( I0, I1, O0 )
    jump( 0 )

def test_asm():
    mem, seq, din, dout = assemble(prog, LOGN, LOGNI, LOGNO)
    disassemble(mem)
