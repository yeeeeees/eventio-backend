
import requests 
from bs4 import BeautifulSoup as bs4    
from selenium import webdriver
import os

name = []
loc = []
time = []
events = []
image = []

URL = "https://adriaticket.com/"

driver = webdriver.Chrome('C:/Users/PC/Downloads/chromedriver_win32/chromedriver.exe')
driver.get(URL)

# r = requests.get(URL) 
r = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

soup = bs4(r, 'html.parser')
events_holder = soup.find_all('div',{'class':'col-md-6 col-sm-6 col-xs-12 one-event ng-scope'})


for event in events_holder:

    events.append('https://www.eventim.hr/' + event.a.get('href'))

for event in events:

    driver = webdriver.Chrome('C:/Users/PC/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get(event)

    r = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = bs4(r, 'html.parser')
    try:
        image_holder = soup.find('div', class_='col-md-8') 
        image.append(image_holder.div.text)
    except AttributeError:
        image.append(None)
    print(image)




