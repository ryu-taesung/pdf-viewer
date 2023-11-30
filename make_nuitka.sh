#!/bin/sh

#--nofollow-import-to=tkinter
#--file-reference-choice=original
python3 get_git_version_tag.py
python3 -m nuitka --standalone --onefile --enable-plugin=pyside6 --include-data-files=version.txt=. --include-data-files=file-pdf.png=. pdf_viewer.py
