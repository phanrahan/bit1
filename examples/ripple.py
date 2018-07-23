import magma as m
import mantle
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NR = 4
NI = NR
NO = NR + 4

def prog():
    from bit1.isa import not_, if1, jump
    for i in range(NR):
        not_(i, i)
        if1(i, 0)
    jump( 0 )


megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.LED.on(NO-NR)

main = megawing.main()

clock = mantle.Counter(22) 

bit1 = Bit1( prog, N, NI, NO, has_ce=True )

O = bit1( bit1.O[:NR], ce=clock.COUT )
m.wire( bit1.O[NR:], main.LED )

