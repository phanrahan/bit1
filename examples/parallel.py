import magma as m
import mantle
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 1
NO = 2

def prog():
    from bit1.isa import out
    out( [0, 0] )
    out( [1, 0] )
    out( [0, 1] )
    out( [1, 1], jump=0 )


megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.LED.on(NO)

main = megawing.main()

clock = mantle.Counter(24) 

bit1 = Bit1(prog, N, NI, NO, mode='parallel', has_ce=True )

m.wire( bit1( m.bits(1,1), ce=clock.COUT ), main.LED )

