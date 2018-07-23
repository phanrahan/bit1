from magma.bitutils import clog2
from bit1.asm import assemble
from bit1 import DefineSeq

N = 32
LOGN = clog2(N)

NI = 2
LOGNI = clog2(NI)

NO = 2
LOGNO = clog2(NO) + 1

def main():
    from bit1.isa import and_, jump, I0, I1, O0
    and_( I0, I1, O0 )
    jump( 0 )

def test_seq():
    _, control, _, _ = assemble(main, LOGN, LOGNI, LOGNO)

    seq = DefineSeq(control, LOGN)
    assert len(seq.O) == LOGN
    print(seq)
