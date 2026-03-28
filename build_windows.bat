@echo off
REM ============================================
REM Build script for Windows 11 (x86_64)
REM ============================================
echo Building Wolf God for Windows 11...

REM Check dependencies
echo Checking dependencies...
pip install pygame pyinstaller --quiet

REM Generate sound files
echo Generating sound files...
python generate_music.py
python generate_sfx.py

REM Clean old build
echo Cleaning old builds...
if exist build rmdir /s /q build
if exist dist\WolfGod_windows rmdir /s /q dist\WolfGod_windows
if exist dist\WolfGod_windows.zip del /f dist\WolfGod_windows.zip

REM Build exe with PyInstaller
echo Building exe...
pyinstaller --noconfirm --windowed ^
    --name "WolfGod_windows" ^
    --add-data "bgm.wav;." ^
    --add-data "coin.wav;." ^
    --add-data "explode.wav;." ^
    main.py

REM Zip the output folder
echo Zipping output...
powershell -Command "Compress-Archive -Path dist\WolfGod_windows -DestinationPath dist\WolfGod_windows.zip -Force"

echo.
echo Build complete!
echo Output: dist\WolfGod_windows\WolfGod_windows.exe
echo Output: dist\WolfGod_windows.zip
echo.
echo Share dist\WolfGod_windows.zip with Windows 11 users
pause