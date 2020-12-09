@ECHO OFF
ECHO Congratulations! Your first batch file executed successfully.
rem echo. 2>EmptyFile.txt
del EmptyFile.txt

del migrations /F /Q
del __pycache__ /F /Q
del data.db /F /Q

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
