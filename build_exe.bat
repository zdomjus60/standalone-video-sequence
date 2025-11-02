@echo off
setlocal enabledelayedexpansion

echo Cleaning up old builds...
rmdir /s /q dist build
del standalone_video_with_audio.spec

set PYINSTALLER_CMD=pyinstaller --onefile standalone_video_with_audio.py

rem Add data files
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "videolist.txt;."

rem Add all .mp4 files found in the directory
for %%f in (*.mp4) do (
  if exist "%%f" (
    set PYINSTALLER_CMD=!PYINSTALLER_CMD! --add-data "%%f;."
  )
)

rem Add all .mp3 files found in the directory
for %%f in (*.mp3) do (
  if exist "%%f" (
    set PYINSTALLER_CMD=!PYINSTALLER_CMD! --add-data "%%f;."
  )
)

echo ------------------------------------------------
echo Building with the following command:
echo %PYINSTALLER_CMD%
echo ------------------------------------------------

!PYINSTALLER_CMD!

if %errorlevel% neq 0 (
    echo --- PYINSTALLER FAILED ---
    goto :eof
)

echo Build complete! The standalone executable is in 'dist/'
echo.
pause
endlocal