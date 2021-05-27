#!/bin/bash

skill_corrections="skill_corrections.csv"
version=$1

echo Building version $version
sub=_
version="${version/./$sub}"
archive_name="Utsushis-Charm_v${version}_linux.zip"


rm -f $archive_name
rm -rf "./build"
rm -rf "./dist"
mkdir -p dist/inputs

source ./env/bin/activate && python -m PyInstaller ./utsushis-charm.spec --onefile

cp $skill_corrections "./dist/$skill_corrections"
chmod +x dist/utsushis-charm

zip $archive_name -r dist/*