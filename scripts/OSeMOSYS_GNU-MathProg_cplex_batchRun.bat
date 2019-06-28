@echo off
setlocal EnableDelayedExpansion

REM the for-loop is for (1 start position, 1 how many steps to jump each time, until which number)
for /L %%j in (1,1,1) do (
	
	REM codename is the name of the OSeMOSYS model, filename is the name of DD file and lpName is the name of the output from glpsol
	SET filename=data_%%i.txt
	SET codename=model.txt
	SET lpName=matrix_%%i.lp
	REM this command starts glpsol
		START /B CMD /C CALL glpsol -m model.txt -d data_%%i.txt --wlp matrix_%%i.lp
	
	REM checks if the lp file is in the folder
	call :waitfile "!lpName!"
	REM lp file is found, but wait 180 sek to make sure the file is built and then kill glpsol
	ECHO Found file !lpName!
	TIMEOUT /T 300 >nul
	ECHO Will kill process now
	taskkill /f /im glpsol.exe
	TIMEOUT /T 10 >nul
	ECHO Process is killed
	REM break mean make a new empty file for mycplexcommands
	break>mycplexcommands
	REM echo writes each line to mycplexcommands that I want to execute in CPLEX
	(
	echo read matrix_%%i.lp
	echo optimize
	echo write
	echo solution_%%i.sol
	echo quit
	) > mycplexcommands

	REM executes the cplex script written above
	cplex < mycplexcommands
	REM the sol file is input to transform python script
	python transform_31072013.py solution_%%i.sol solution_%%i.txt
	REM the transform txt file is input to the Results file that adds to a Accessdatabase
	
	sort/+1<solution_%%i.txt>solution_%%i_sorted.txt

	REM delete lp and sol file
	del matrix_%%i.lp
	del solution_%%i.sol
	del solution_%%i.txt

)

ECHO All done!
exit /b 0

REM this command is active as long as glpsol is building the lp file (will be printed every 120 sek)
:waitfile
    ECHO waitforfile: %~1
:waitfile2
	ECHO Waiting...
    TIMEOUT /T 300 >nul
    IF not EXIST "%~1" goto waitfile2
exit /b 0
