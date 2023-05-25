@ECHO OFF

title Compile for distribution

:: file name
set fname=GUI_OIS_Analyzer

:: version 변수 초기화
set version=

:REDO
set /p version=버전을 입력하세요 :
if "%version%" == "" goto REDO

copy "..\[Function] New Function file\HK_func_file_folder_control.py"
copy "..\[Function] New Function file\HK_func_image_movie_file_control.py"

"C:\Program Files\Python39\Scripts\pyinstaller" --noconfirm --windowed --onedir --icon=.\LG.ico %fname%.py --name %fname%_%version% --add-data "%fname%.ui;." --add-data "LG.ico;."

del .\HK_func_file_folder_control.py
del .\HK_func_image_movie_file_control.py

 
echo ##### Finished !!! #####
pause

