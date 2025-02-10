# Overview
Cross compatible app that will serve as the center point for all insensitive data.

# COMMAND TO COMPILE: 
pyinstaller --onefile  --hidden-import=controllers --hidden-import=win32timezone --collect-submodules=controllers --collect-submodules=kivymd test_main.py

# Fixes: 
[x] give option to send a new email or reply to the last one.
[x] main page shows if it is customer or supplier
[x] email popup needs to show who the email was from.
[x] email popup date formatting improvement
[ ] enable secret scanning in the github repo and then push to main.
[ ] reply tab should show the thread of the last email in the outlook client.
[x] date format should be USA + show time (12 hours)
[x] change name to party name in the main page of the application

# Pulling data as <party_name>: [ list of email_ids ]
[ ] email_item_class needs a parent class with the party_name. (EmailItems will go inside it.
[ ] script to pull from SQL
    [ ] Parents = pull all the unique partyfks from the partbuyer table
    [ ] Children = buyerfk (multiple) for one partyfk in partybuyer
        then buyerfk = partypk in the party table.
[ ] change scripts.py
    [ ] add script
    [ ] use parent class to create EmailItem children
    [ ] change the structure of the config files.


# EXE fixes: 
[ ] remove terminal window and shift logs to a folder. (need to read more about how these logs are streamed to where) 
[ ] fix .env file not compiling with runtime
