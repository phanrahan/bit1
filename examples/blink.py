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
megawing.LED.on(NO)

main = megawing.main()
if NO == 1:
    main.LED = m.bits([main.LED])

slow = mantle.Counter(24) 

# clr, set at slow clock
def prog():
    from bit1.isa import clr, set, O0
    clr( O0 )
    set( O0, jump=0 )

bit1 = Bit1(prog, N, NI, NO, has_ce=True )

m.wire( bit1( m.bits(1,1), ce=slow.COUT ), main.LED )

