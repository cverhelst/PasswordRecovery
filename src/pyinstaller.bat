@echo off

set PIP=C:\Python27\pyinstaller-1.5
set mydir=%2

for /f "tokens=1-10 delims=\" %%A in ("%mydir%") do (
    if NOT .%%A==. set new=%%A
    if NOT .%%B==. set new=%%B
    if NOT .%%C==. set new=%%C
    if NOT .%%D==. set new=%%D
    if NOT .%%E==. set new=%%E
    if NOT .%%F==. set new=%%F
    if NOT .%%G==. set new=%%G
    if NOT .%%H==. set new=%%H
    if NOT .%%I==. set new=%%I
    if NOT .%%J==. set new=%%J
)

for /f "tokens=1 delims=." %%Z in ("%new%") do (
	set file=%%Z
)

set install=%1/%file%EXE

python %PIP%\Makespec.py -p %1 -o %install% %2
python %PIP%\Build.py %install%\%file%.spec

