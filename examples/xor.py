import magma as m
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 2
NO = 1

def prog():
    xor( I0, I1, O0 )
    jump( 0 )


megawing = MegaWing(PapilioPro)
megawing.Clock.on()
megawing.Switch.on(NI)
megawing.LED.on(NO)

main = megawing.main()
if NI == 1:
    main.SWITCH = m.bits([main.SWITCH])
if NO == 1:
    main.LED = m.bits([main.LED])

bit1 = Bit1(prog, N, NI, NO )
m.wire( bit1(main.SWITCH), main.LED )

