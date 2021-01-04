@echo off
:LOOP
%~n0.py
rem if not %errorlevel%==0 goto LOOP
pause
