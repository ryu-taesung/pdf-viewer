#!/bin/sh
################################################################################
############################# make_pyinstaller.sh ##############################
################################################################################

python3 get_git_version_tag.py
pyinstaller --windowed --add-data="file-pdf.png:." --add-data="version.txt:." --icon="file-pdf.png" --noconfirm pdf_viewer.py
