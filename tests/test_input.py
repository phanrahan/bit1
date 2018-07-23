import pytest
from magma.bitutils import clog2
from bit1.asm import assemble
from bit1 import DefineInput

N = 32
LOGN = clog2(N)

NO = 2
LOGNO = clog2(NO) + 1

def main():
    from bit1.isa import and_, jump, I0, I1, O0
    and_( I0, I1, O0 )
    jump( 0 )

@pytest.mark.parametrize("NI", [2,4,8,16])
def test_input(NI):
    LOGNI = clog2(NI)
    _, _, din, _ = assemble(main, LOGN, LOGNI, LOGNO)

    input = DefineInput(din, LOGN, LOGNI)
    assert len(input.pc) == LOGN
    assert len(input.I) == NI
    print(input)
