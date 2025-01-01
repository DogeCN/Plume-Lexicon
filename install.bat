@echo off
pyinstaller --noconfirm --onefile --windowed --icon ".source\icon.ico" --optimize "2" --disable-windowed-traceback --version-file "dist\version.txt"  "main.py"
taskkill>nul 2>nul /im "Plume Lexicon.exe" /f
timeout /t 1 /nobreak > nul
del "dist\Plume Lexicon.exe"
ren dist\main.exe "Plume Lexicon.exe"
echo 99999 INFO: Plume Lexicon.exe Completed.
