# JGDJSS created by Deepak Lohia on 23-Apr-2022
# Python script to Control your chrome browser using selenium 
# RUN pip install selenium  https://pypi.org/project/selenium/
# download selenium driver from https://chromedriver.chromium.org/home as per ur chrome version and place "chromedriver" in "C:\temp"  and start once
# you may change location as per ur choice and amend the path below

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#change as per requirement
chrome_path = "C:\\temp\\chromedriver"
email = "abc@example.com"
password  = "xxxx123456"
url = "https://www.yourbrowser.com/sign_in"

print("process Started")

op = Options()
#op.binary_location = chrome_path    #chrome binary location specified here
op.add_argument("--start-maximized") #open Browser in maximized mode
#op.add_argument("--no-sandbox") #bypass OS security model
op.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('useAutomationExtension', False)
op.headless = False # change to true if we want to hide the browser
s = Service(chrome_path)

with  webdriver.Chrome(service=s, options=op) as d:
    d.get(url)
    d.find_element(By.ID, "user_email_login").send_keys(email)
    d.find_element(By.ID, "user_password").send_keys(password)
    time.sleep(60)
    #d.find_element(By.ID, "user_submit").click()
    time.sleep(4000)  # wait

print ("Done")