# Instapoll-Bot Instructions
# download webdriver (some code might need to be changed if not for chrome).
# pip install selenium, and twilio, as well as make new .py file called very_public_info.py
# which has 4 variables (eid, pass1, sid, and token). eid and pass1 will be your UT login info.
# sid and token will come after you set up a free Twilio account (choose the "no code" option).
# the "Account SID" and "Auth Token" should show up on your dashboard once you have created an account.
# you will then "purchase" a phone number through Twilio and follow the instructions to register an address.
# then create a "studio flow" that's empty and connect it to your Twilio phone number for incoming calls and texts.
# the last step is to add the new Twilio phone number to Duo (just add, don't replace).
# BE SURE TO SET IT AS THE DEFAULT NUMBER.
# Normal Duo functionality will not change on the app, and if you want text/call notifications for normal logging in,
# simply choose the second number (your actual number) in the drop down box.
