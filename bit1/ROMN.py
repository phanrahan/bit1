from collections import Sequence
from magma import *
from mantle import LUT5, LUT6, LUT7, FF

__all__  = ['ROM']

# Construct a ROM of arbitrary height and width
#
#   rom[1<<height][width]
#
# The ff flag indicates whether the ROM output should have a register.
#
def ROM(rom, height, width, ff=False, has_ce=False, has_reset=False):

    assert 5 <= height <= 7
    assert 1 << height == len(rom)

    # transpose
    rom = list(zip(*rom))
    assert width == len(rom)

    def _ROM(y):
        if   height == 7:
            lut = uncurry(LUT7(rom[y]))
        elif height == 6:
            lut = uncurry(LUT6(rom[y]))
        elif height == 5:
            lut = uncurry(LUT5(rom[y]))
        if ff:
            reg = FF(has_ce=has_ce, has_reset=has_reset)
            reg(lut.O)
            args = ["I", lut.I, "O", reg.O] + reg.clockargs()
            return AnonymousCircuit(args)
        else:
            reg = lut
        return reg

    return fork(col(_ROM, width))
