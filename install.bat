@echo off
pyinstaller main.spec --noconfirm
echo 99998 INFO: Updating main.exe
rem "dist\Plume Lexicon\bin\main.exe"
copy >nul "dist\installed\main.exe" "dist\Plume Lexicon\bin\"
echo 99999 INFO: Completed.
