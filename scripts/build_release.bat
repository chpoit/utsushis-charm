@echo off
set tesseract_name="tesseract-installer.exe"
set skill_corrections="skill_corrections.csv"
set version=%1
set version=%version:.=_%
set archive_name="Utsushis-Charm_v%version%.zip"

echo "Building version %version%"

del %archive_name%
rd /s /q "build"
rd /s /q "dist"
md dist
md "dist\inputs"

cmd /c ".\env\scripts\activate & python -m PyInstaller .\utsushis-charm.spec --onefile & .\env\scripts\deactivate;" 

copy %skill_corrections% "dist\%skill_corrections%"

if not exist %tesseract_name% (
    echo "Tesseract installer missing, downloading..."
    curl https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe -o %tesseract_name%
)

copy %tesseract_name% "dist\%tesseract_name%"

7z a -tzip %archive_name% ".\dist\*"
