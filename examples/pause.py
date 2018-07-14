import magma as m
import mantle
from mantle.util.debounce import debounce
from mantle.util.edge import falling
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 1
NO = 2

def prog():
    clr( 0 )
    pause( 0 )
    set( 0 )
    pause( 0 )
    jump( 0 )


megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.Joystick.on()
megawing.LED.on(NO)

main = megawing.main()
if NO == 1:
    main.LED = m.bits([main.LED])

slow = mantle.Counter(16)
select = debounce( main.SELECT, slow.COUT )
step = falling(select)

bit1 = Bit1(prog, N, NI, NO)

m.wire( bit1( m.bits([step]) ), main.LED )

