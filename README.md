# Overview
Cross compatible app that will serve as the center point for all insensitive data.

# COMMAND TO COMPILE: 
pyinstaller --onefile  --hidden-import=controllers --hidden-import=win32timezone --collect-submodules=controllers --collect-submodules=kivymd test_main.py

# Fixes: 

[ ] give option to send a new email or reply to the last one.
[ ] main page shows if it is customer or supplier
[ ] email popup needs to show who the email was from.
[ ] email popup date formatting improvement

# EXE fixes: 
[ ] remove terminal window and shift logs to a folder. (need to read more about how these logs are streamed to where) 
[ ] fix .env file not compiling with runtime
