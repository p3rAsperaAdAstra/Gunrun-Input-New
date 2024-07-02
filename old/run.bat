@echo off
REM set the directory of Gudrun as an Environmental variable
set _dir=D:\GudrunGUI-2022.3-Windows64
REM run python sript to create input.txt and GudrunX_windows.syspar for Gudrun
python input.py
REM copy GudrunX_windows.syspar to Gudrun folder
copy GudrunX_windows.syspar %_dir%GudrunX_windows.syspar
del GudrunX_windows.syspar
REM change directory to Gudrun
cd /d %_dir%
REM run GudrunX batch file
gudrunx 

REM In Windows Command-Prompt the syntax is echo %PATH%

REM To get a list of all environment variables enter the command set

REM To send those variables to a text file enter the command set > filename.txt
@echo on