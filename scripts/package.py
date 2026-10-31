#!/usr/bin/env python3
"""Deterministic four-file Super Productivity plugin package."""
from pathlib import Path
import argparse
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
NAMES=("manifest.json","plugin.js","index.html","icon.svg")

def build(tag=None):
    folder=ROOT/"plugin"
    manifest=json.loads((folder/"manifest.json").read_text())
    assert manifest["id"]=="sp-deadline-watch"
    assert manifest["iFrame"] is True
    if tag and tag!="v"+manifest["version"]:
        raise ValueError("Tag must match manifest version")
    assert set(p.name for p in folder.iterdir() if p.is_file())==set(NAMES)
    output=ROOT/"dist"/"deadline-watch-super-productivity.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in NAMES:
            item=zipfile.ZipInfo(name,(2026,1,1,0,0,0))
            item.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(item,(folder/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist()==list(NAMES)
        assert archive.testzip() is None
    print(output)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--tag")
    args=parser.parse_args()
    build(args.tag)
