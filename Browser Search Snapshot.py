#JGDJSS Designed by Deepak Lohia on 24th April 2022
#Automation to open browser / read content and take a snapshot

'''
download driver from  
https://sites.google.com/chromium.org/driver/downloads
'''

import glob
import time
import os
import socket
#pip install selenium
from selenium import webdriver
#from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
#pip install webdriver-manager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

 # pip3 install Selenium-Screenshot  
# #ref https://pypi.org/project/Selenium-Screenshot/
from PIL import Image
from Screenshot import Screenshot_Clipping

bPath = os.getcwd()
inputFile = bPath + '/input.txt'
outputFile = bPath + '/output.txt'
baseURL = "https://www.google.com/"
chrome_path = bPath  + '//driver//chromedriver.exe' 
#chrome_path = chrome_path.replace('\\' , '\\\\')
#chrome_path = os.path.normpath(bPath + os.sep + os.pardir) +  "\driver\chromedriver.exe"       #gettig one step back folder

def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False

#check internet
if is_connected("baseURL") == True:
    print("no internet")
    exit()

fURL = ""
input_items = []
#clear output file

open(outputFile, 'w').close()

with open(inputFile, "r") as i:  # use r for read
    for ln in i.readlines():
        input_items.append(ln.replace("\n", ""))
i.close()

data = False
for searchItem in input_items:
    data = True

if data == False:
    print ('no data in "input" file')
    exit()

#deleting existing images
files = glob.glob(bPath +  "/snaps/*" )
for f in files:
    os.remove(f)
print ("existing images cleared...")

print("process Started")

op = Options()
#op.binary_location = chrome_path    #chrome binary location specified here
op.add_argument("--start-maximized") #open Browser in maximized mode
#op.add_argument("--no-sandbox") #bypass OS security model
op.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('useAutomationExtension', False)
#op.add_experimental_option('excludeSwitches', ['enable-logging'])
op.headless = False

s = Service(chrome_path)

with  webdriver.Chrome(service=s, options=op) as d:
    for searchItem in input_items:
        #print("loading browser...")
        url = "allintitle:" + searchItem
        url = "https://www.google.com/search?q={}".format(url)

        #FOR YOUR OWN WEBSITE
        #url = "yoursite?abc= " + searchItem

        d.get(url)
        d.maximize_window()
        time.sleep(3)

        print ("opening ...." +  url)

        imgName = format(searchItem)
        imgName = imgName.replace(" ", "_")
        imgName = imgName.replace ( '"', '')
        imgName = imgName.replace("\n","")
        imgName = imgName.replace('"','') 
        imgName = imgName.replace ('/' , '')
        imgPath  = bPath +  "/snaps/" + imgName +  ".png"
        d.save_screenshot(imgPath)

        '''
        original_size = d.get_window_size()
        required_width = d.execute_script('return document.body.parentNode.scrollWidth')
        required_height = d.execute_script('return document.body.parentNode.scrollHeight')
        d.set_window_size(required_width, required_height)
        time.sleep(1)
        #d.save_screenshot(imgPath)  # has scrollbar
        #d.find_element ( By.TAG_NAME , "body").screenshot(imgPath)  # avoids scrollbar
        #d.set_window_size(original_size['width'], original_size['height']) #reverse back browser size
        time.sleep(1)
        '''
        #time.sleep(3)
        try:
            text  = d.find_element ( By.ID , "result-stats").text
            #text  = d.find_element ( By.TAG_NAME , "body").get_attribute("outerHTML")
        except:
            text = "No Data"

        result =  text + " | " + imgPath
        
        # extracting latitude, longitude and formatted address 
        # of the first matching location
        o = open(outputFile, "a")  
        #o.writelines(fURL + " | "   +  result +  " | " +  result2 + "\n")
        #o.writelines( result +  " | " +  result2 + "|" +  fURL + "\n")
        o.writelines( searchItem + "|" + result + "|" + url +  "\n")
        o.close()

        time.sleep(1)
        
d.quit()
print("******DONE********************")