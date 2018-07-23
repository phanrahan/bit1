mov.py
  mov(I0, O0)
not.py
  not_(I0, O0)

and.py
  and_(I0, I1, O0)
or.py
  or_(I0, I1, O0)
xor.py
  xor(I0, I1, O0)

blink.py : ce=slow 
  clr( O0 )
  set( O0, jump=0 )

blinkstep.py : ce=debounce(button)
  clr( O0 )
  set( O0, jump=0 )

pause.py
  clr
  pause(I0)
  set
  pause(I0)
  jump(0)

oneshot.py

ripple.py

