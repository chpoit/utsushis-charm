@echo off
set skill_corrections="skill_corrections.csv"
set version=%1
echo "Building version %version%"

set version_str=%version:.=_%
set archive_name="Utsushis-Charm_v%version_str%.zip"

python .\scripts\update_ver.py %version%

del %archive_name%
rd /s /q "build"
rd /s /q "dist"
md dist
md "dist\inputs"

cmd /c ".\env\Scripts\activate & python -m PyInstaller .\utsushis-charm.spec & .\env\scripts\deactivate;" 

7z a -tzip %archive_name% ".\dist\*"
