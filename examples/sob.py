import magma as m
import mantle
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 1
NO = 1

def prog():
    ZERO = I0
    TICK = O0

    sob(TICK,ZERO)
    jump(0)

megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.LED.on(4)

main = megawing.main()

clock = mantle.Counter(24) 
counter = mantle.Counter(4, has_ce=True)
bit1 = Bit1(prog, N, NI, NO, has_ce=True) 
print(str(type(bit1)))

O = bit1( m.bits([counter.COUT]), ce=clock.COUT )

# Note: counter returns O, COUT
m.wire( counter(ce=O[0])[0], main.LED ) 


