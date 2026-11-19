#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119 (Python 3.13, stdlib only).

The front page is the entry.png beside this file, drawn by
build_frontpage.py from the verified news of Thursday 19 November 2026.
This program copies it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
No network access; the same bytes are written on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
dest = os.path.join(OUT, "entry.png")
shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
size = os.path.getsize(dest)
assert size < 1024 * 1024, "entry.png exceeds the 1 MiB gate"
print(f"wrote {dest} ({size} bytes)")
