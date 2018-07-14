import magma as m
import mantle
from loam.boards.papiliopro import PapilioPro
from loam.shields.megawing import MegaWing
from bit1 import Bit1

N = 32
NI = 1
NO = 2

def prog():
    ZERO = I0

    # mode [0, 0]
    #  SCLK idle state is 0
    #  data is clocked in on the SDI pin on the rising edge of SCK 
    #  and clocked out on the SDO pin on the falling edge of SCK.
    inst([0, 0])
    inst([1, 0])
    inst([0, 0], ZERO, label()-1 )
    #inst([0, 1], jump=0)
    inst([0, 1], jump=label())

    # Mode = [1,1]
    #  SCK idle state = high (VIH),
    #  data is clocked in on the SDI pin on the rising edge of SCK 
    #  and clocked out on the SDO pin on the falling edge of SCK.
    #out(  1,0, 0)
    #inst([0,0, 0])
    #inst([1,1, 0])
    #inst([0,0, 0])
    #inst([1,1, 0], ZERO, label()-1 )
    #out(  1,0, 1,  jump=label()) # halt


papilio = PapilioPro()
papilio.Clock.on()
for i in range(3):
    papilio.A[i].output().on()

main = papilio.main()

clock = mantle.Counter(6)()
reset = clock.COUT
counter = mantle.Counter(5, has_ce=True)
mosi = mantle.PISO(16, has_ce=True) 
bit1 = Bit1(main, N, NI, NO, mode='parallel', has_reset=True))

sclk, ss = bit1(counter.O[4], reset=reset)

counter(ce=sclk)

mosi( 0, m.bits(1,16), reset, ce=reset|sclk )

m.wire( ss,   main.A[0] )
m.wire( sclk, main.A[1] )
m.wire( mosi.O, main.A[2] )

