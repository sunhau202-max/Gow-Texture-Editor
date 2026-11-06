@echo off
title Build - Gow Language Editor by Nicho
python -m pip install --upgrade pip pyinstaller
python -m PyInstaller --noconfirm --onedir --windowed --name Texture_Editor --icon icon.ico gow_texture_tool.py
if errorlevel 1 goto fail

rem Rakit paket: Texture Editor\ (folder program) + txt di sebelahnya
if exist "paket" rmdir /s /q "paket"
mkdir "paket"
xcopy /e /i /y "dist\Texture_Editor" "paket\Texture Editor" >nul
for %%F in (Readme-Indo.txt Readme-Eng.txt Leia-me-Br.txt Informasi-Indo.txt Information-Eng.txt Informacoes-Br.txt) do copy /y "%%F" "paket\" >nul
echo.
echo Selesai. Hasil ada di folder "paket" (zip isinya menjadi "Texture Editor.zip").
pause
exit /b 0

:fail
echo Build gagal.
pause
exit /b 1
