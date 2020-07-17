from bs4 import BeautifulSoup
import urllib3
from datetime import datetime
from openpyxl import load_workbook
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

options = webdriver.ChromeOptions() 
#options.add_argument(r'''user-data-dir=C:\Users\Tarik's PC\AppData\Local\Google\Chrome\User Data''')
#"user-data-dir=C:\Users\Tarik's PC\AppData\Local\Google\Chrome\User Data" home
# "user-data-dir=C:\Users\koric1\AppData\Local\Google\Chrome\User Data" work
#options.add_argument("--start-maximized")
#self.options.add_argument("--headless")
#self.options.add_argument("--no-sandbox")
#self.options.add_argument("--disable-gpu")
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessa
driver = webdriver.Chrome(chrome_options= options)

with open('kenpom.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["team","off","def","tempo","luck"])
    #writer.writerow(["SN", "Name", "Contribution"])
    driver.get('https://kenpom.com/')
    time.sleep(1)
    
    for x in range(1,10):
        try:
            for z in range(1,41):
                
                team_name = str(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[2]/a').text)
                team_off = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[6]').text)
                team_def = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[8]').text)
                team_t = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[10]').text)
                team_luck = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[12]').text)
                print(team_name,team_off,team_def,team_t,team_luck)
                writer.writerow([team_name,team_off,team_def,team_t,team_luck])
        except:
            break
driver.close()

