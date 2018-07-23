import magma as m
import mantle
from mantle.util.debounce import debounce
from mantle.util.edge import falling
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 1
NO = 8

def prog():
    from bit1.isa import set, clr, halt
    for i in range(NO):
        j = (i-1+NO) % NO
        set( i )
        clr( j ) 
    clr( NO-1 )
    halt()


megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.Joystick.on()
megawing.LED.on(NO)

main = megawing.main()

slow = mantle.Counter(16)
select = debounce( main.SELECT, slow.COUT )
step = falling(select)

clock = mantle.Counter(24) 

bit1 = Bit1(prog, N, NI, NO, has_ce=True, has_reset=True )

m.wire( bit1( m.bits(0,1), ce=clock.COUT, reset=step ), main.LED )

