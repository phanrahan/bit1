from .asm import inst, getpc, setpc, org, equ, label

I0 = 0
I1 = 1
I2 = 2
I3 = 3
I4 = 4
I5 = 5
I6 = 6
I7 = 7
I8 = 8
I9 = 9
I10 = 10
I11 = 11
I12 = 12
I13 = 13
I14 = 14
I15 = 15

O0 = 0
O1 = 1
O2 = 2
O3 = 3
O4 = 4
O5 = 5
O6 = 6
O7 = 7
O8 = 8
O9 = 9
O10 = 10
O11 = 11
O12 = 12
O13 = 13
O14 = 14
O15 = 15


def jump( pc ):
    inst( None, 0, jump=pc )

def halt():
    jump( getpc() )


# if port == 0:
#   jump(pc)
def if0( port, pc ):
    inst( None, port, next_pc0=pc )

# if port == 1:
#   jump(pc)
def if1( port, pc ):
    inst( None, port, next_pc1=pc )

# jump(pc1 if port else pc0)
def ifelse( port, next_pc1, next_pc0 ):
    inst( None, port, next_pc0=next_pc0, next_pc1=next_pc1 )

# skip n instructions
def skip( n=1 ):
    inst( None, skip=n )

# if port == 0: 
#   skip next instruction
def skipif0( port, n=1 ):
    inst( None, port, next_pc0=getpc(n+1), next_pc1=getpc(1) )

# if port == 1: 
#   skip next instruction
def skipif1( port, n=1 ):
    inst( None, port, next_pc1=getpc(n+1), next_pc0=getpc(1))

# loop at the current location until port is true
def pause( port ):
    inst( None, port, next_pc0=getpc(), next_pc1=getpc(1) )


def out( args, **kwargs):
    inst( args, **kwargs )

def clr( port, **kwargs ):
    out( [port, 0], **kwargs )

def set( port, **kwargs ):
    out( [port, 1], **kwargs )


def nop():
    inst( None )

def delay(n):
    for i in range(n):
        nop()


def mov( ra, rb ):
    skipif1( ra )
    clr( rb, skip=1 )
    set( rb )

def not_( ra, rb ):
    skipif0( ra )
    clr( rb, skip=1 )
    set( rb )

def and_( ra, rb, rc ):
    skipif0( ra, 2 )
    skipif0( rb, 1 )
    set( rc, skip=1 )
    clr( rc )

def or_( ra, rb, rc ):
    skipif1( ra, 2 )
    skipif1( rb, 1 )
    clr( rc, skip=1 )
    set( rc )

def xor( ra, rb, rc ):
    skipif1( ra, 1 )
    ifelse( rb, getpc(2), getpc(3) ) # ra=0
    ifelse( rb, getpc(2), getpc(1) ) # ra=1
    set( rc, skip=1 ) # ra != rb
    clr( rc )         # ra == rb

