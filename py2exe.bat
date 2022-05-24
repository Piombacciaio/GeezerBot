@echo off
cls
title converting py to exe
pyinstaller --onefile main.py --n GeezerBot
title conversion completed
pause