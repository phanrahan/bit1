import pytest
from magma.bitutils import clog2
from bit1.asm import assemble
from bit1 import DefineDecodedOutput, DefineOutput

N = 32
LOGN = clog2(N)

NI = 2
LOGNI = clog2(NI)

def main():
    from bit1.isa import and_, jump, I0, I1, O0
    and_( I0, I1, O0 )
    jump( 0 )

@pytest.mark.parametrize("NO", [1,2,3,4,5,6,7,8,16])
def test_decoded_output(NO):
    if NO == 1:
        LOGNO = clog2(NO+1) + 1 
    else:
        LOGNO = clog2(NO) + 1 
    _, _, _, dout = assemble(main, LOGN, LOGNI, LOGNO)

    output = DefineDecodedOutput(dout, LOGN, LOGNO, NO)
    assert len(output.pc) == LOGN
    assert len(output.O) == NO
    #print(output)

@pytest.mark.parametrize("has_ce", [False, True])
@pytest.mark.parametrize("has_reset", [False, True])
def test_decoded_clock(has_ce, has_reset):
    NO = 2
    LOGNO = clog2(NO) + 1 
    _, _, _, dout = assemble(main, LOGN, LOGNI, LOGNO)

    output = DefineDecodedOutput(dout, LOGN, LOGNO, NO, 
                 has_ce=has_ce, has_reset=has_reset)
    assert len(output.pc) == LOGN
    assert len(output.O) == NO
    assert not has_ce or hasattr(output, 'CE')
    assert not has_reset or hasattr(output, 'RESET')
    #print(output)

@pytest.mark.skip(reason='NYI')
@pytest.mark.parametrize("NO", [1,2,3,4,5,6,7,8,16])
def test_output(NO):
    LOGNO = NO
    _, _, _, dout = assemble(main, LOGN, LOGNI, LOGNO, mode='parallel')

    output = DefineOutput(dout, LOGN, NO)
    assert len(output.pc) == LOGN
    assert len(output.O) == NO
    #print(output)
