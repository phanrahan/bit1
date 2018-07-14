from magma.shield.LogicStart import *
from mantle.bits import itob
from laughton import *

def main():
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




# 4Mhz
#wire( DCM(4,site=(0,2)) (In(94)), curDesign.CLKIN )
Papilio.Clock(4)

A0 = Out(Papilio.A[0])
A1 = Out(Papilio.A[1])
A2 = Out(Papilio.A[2])

reset = Counter(6, cout=True, site=(0,2))(1) [6]
    
N = 4
i = itob((1<<N)-1, N)
counter = Counter(N, init=i, cout=True, site=(2,2))
count = counter(1, ce=None)

sclk = Wire()
ss = Wire()

I = [count [N]]
O = [sclk, ss]

bit1 = Laughton(main, len(I), len(O), output='parallel', r=True, site=(4,2))
wire( bit1(I, r=reset), O )

wire( sclk, counter.CE )

ce = Or(2, site=(1,6))(reset, sclk)
seq = itob( 1, 9 ) + 7 * [0]

mosi = PISO(16, site=(1,2)) ( 0, seq, reset, ce=ce )

wire( ss,   A0 )
wire( sclk, A1 )
wire( mosi, A2 )

