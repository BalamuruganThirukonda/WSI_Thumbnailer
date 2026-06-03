@echo off

REM Activate conda environment
call C:\Users\Public\conda-envs\slideqc\Scripts\activate.bat

REM Go to project directory
cd /d D:\Slides\WSI_Thumbnailer

REM Run script
python main.py

pause