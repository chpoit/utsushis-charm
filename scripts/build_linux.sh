#!/bin/bash

skill_corrections="skill_corrections.csv"
version=$1

echo Building version $version
sub=_
version_str="${version/./$sub}"
archive_name="Utsushis-Charm_v${version_str}_linux.zip"

python ./scripts/update_ver.py %version%

rm -f $archive_name
rm -rf "./build"
rm -rf "./dist"
mkdir -p dist/inputs

source ./env/bin/activate && python -m PyInstaller ./utsushis-charm.spec --onefile

chmod +x dist/utsushis-charm

zip $archive_name -r dist/*