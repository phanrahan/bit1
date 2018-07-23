import magma
magma.set_mantle_target('spartan6')
from magma.bitutils import clog2
from bit1.asm import assemble, disassemble

N = 32
LOGN = clog2(N)

NI = 2
LOGNI = clog2(NI)

NO = 2
LOGNO = clog2(NO) + 1

def prog():
    from bit1.isa import set, clr
    from bit1.isa import mov, not_, and_, or_, xor
    from bit1.isa import nop, delay
    from bit1.isa import jump
    from bit1.isa import if0, if1, ifelse
    from bit1.isa import skip, skipif0, skipif1
    from bit1.isa import halt

    set( O0 )
    clr( O0 )
    mov(  I0, O0 )
    not_( I0, O0 )
    and_( I0, I1, O0 )
    or_( I0, I1, O0 )
    xor( I0, I1, O0 )
    delay(1)
    jump( 0 )
    if0( I0, 0 )
    if1( I0, 0 )
    ifelse( I0, 0, 0 )
    skipif0( I0 )
    #skipif1( I0 )
    skip_( )
    pause( I0 )
    nop()
    halt( )


mem, _, _, _ = assemble(prog, LOGN, LOGNI, LOGNO)
disassemble(mem)


