# instructions!
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

# imports
import time
from selenium import webdriver
from twilio.rest import Client
from selenium.webdriver.common.by import By
from very_public_info import eid, pass1, sid, token
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# opens the Instapoll page and gets past Duo
class CanvasBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # change this URL if you want to do Instapolls for a different class
        self.driver.get("https://utexas.instructure.com/courses/1312338/assignments/5625640")
        # finds fields for eid, password, and submit
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(eid)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(pass1)
        self.driver.find_element_by_xpath('//*[@id="login-button"]/input').click()
        # need to wait for the embedded Duo frame to become available
        WebDriverWait(self.driver, 20).until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='duo_iframe']")))
        # there is a tiny bit of lag between when the frame is available and when we can click the button
        # constant time difference though, so sleep is acceptable here
        time.sleep(2)
        # click the send passcode button
        self.driver.find_element_by_xpath("//*[@id='passcode']").click()
        # get the text that says which code to send
        code_text = self.driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset[1]/div[3]/div/div').text
        # request codes be sent via text
        self.driver.find_element_by_xpath("//*[@id='message']").click()
        time.sleep(1)
        # gain access to Twilio API
        client = Client(sid, token)
        # get most recent message and isolate codes
        sms = client.messages.list()[0].body
        sms = " ".join(sms.split()).split(' ')
        code = ''
        if code_text[-1] == 0:
            # codes starting with 0 are at the end of the list
            code = sms[-1]
        else:
            code = sms[1 + int(code_text[-1])]
        # finds field for codes, inputs the correct code, and submits it
        self.driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset[1]/div[3]/div/input').send_keys(code)
        self.driver.find_element_by_xpath("//*[@id='passcode']").click()
        # wait for the Instapoll button to appear and then click it!
        # this XPATH may need to be updated if using this bot for a different class than 429
        WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="tool_form"]/div/div[1]/div/button'))).click()
        time.sleep(2)
        # even though it opened a new window, it is still on the old window so switch it
        self.driver.switch_to.window(self.driver.window_handles[1])
        # TODO get hidden question
        # loop twice to answer both polls
        for i in range(2):
            WebDriverWait(self.driver, 7200).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="__BVID__7___BV_modal_body_"]/div/div/div[2]/button'))).click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="__BVID__7___BV_modal_footer_"]/button[2]').click()
            print("Did an Instapoll!")
        print("All done!")


# create instance of the bot
bot = CanvasBot()
