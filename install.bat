@echo off
pyinstaller --noconfirm --onefile --windowed --icon ".source\icon.ico" --optimize "2" --disable-windowed-traceback  "main.py"
del "dist\Plume Lexicon.exe"
ren dist\main.exe "Plume Lexicon.exe"
echo 99999 INFO: Plume Lexicon.exe Completed.
