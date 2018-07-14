import magma as m
import mantle
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 1
NO = 1

megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.LED.on(4)

main = megawing.main()

def prog():
    TICK = I0
    COUT = O0

    pause(TICK)
    out(COUT, 1)
    out(COUT, 0, jump=0)

clock = mantle.Counter(24) 
counter = mantle.Counter(4, has_ce=True)

bit1 = Bit1(prog, N, NI, NO) 

O = bit1( m.bits([clock.COUT]) )
m.wire( counter( ce=O[0] )[0], main.LED )

