import pytest
from bit1 import Bit1

N = 32
NI = 2
NO = 2

def main():
    and_( I0, I1, O0 )
    jump( 0 )

@pytest.mark.parametrize('NI', [1,2])
def test_bit1_input(NI):
    bit1 = Bit1(main, N, NI, NO)
    assert len(bit1.I) == NI
    assert len(bit1.O) == NO
    #print(bit1)

@pytest.mark.parametrize('NO', [1,2])
def test_bit1_output(NO):
    bit1 = Bit1(main, N, NI, NO)
    assert len(bit1.I) == NI
    assert len(bit1.O) == NO
#    #print(bit1)

@pytest.mark.parametrize("has_ce", [False, True])
@pytest.mark.parametrize("has_reset", [False, True])
def test_bit1_clock(has_ce, has_reset):
    bit1 = Bit1(main, N, NI, NO, has_ce=has_ce, has_reset=has_reset)
    assert len(bit1.I) == NI
    assert len(bit1.O) == NO
    assert not has_ce or hasattr(bit1, 'CE')
    assert not has_reset or hasattr(bit1, 'RESET')
    #print(output)

