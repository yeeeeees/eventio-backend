import requests 
from bs4 import BeautifulSoup as bs4    
from selenium import webdriver

name = []
loc = []
time = []
events = []
image = []

URL = "https://www.eventim.hr/hr/venues/split/city.html"

driver = webdriver.Chrome('C:/Users/PC/Downloads/chromedriver_win32/chromedriver.exe')
driver.get(URL)

# r = requests.get(URL) 
r = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

soup = bs4(r, 'html.parser')
events_holder = soup.find_all('a',{'class':'m-eventListItem'})

for event in events_holder:
    events.append('https://www.eventim.hr' + event.get('href'))


for event in events:

    driver = webdriver.Chrome('C:/Users/PC/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get(event)

    r = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = bs4(r, 'html.parser')

    image_holder = soup.find('img', class_='pageheader-bgimage') 
    image.append(image_holder.get('src'))

print(image)