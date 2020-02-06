import sys
sys.path.append('/home/proj/eventio-backend')
from app import db
from app.models import Event, User
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import os

def add_to_db(username, titles, times, locs, descs, images):        
    
    duplicate_user = False
    for user in User.query.all():
        if username == user.username:
            duplicate_user = True
            
    if duplicate_user == False:
        extra_user = User(username=username, fname=username, surname=username, email='{}@gmail.com'.format(username), password=username, created_events=[], joined_events=[])      
        db.session.add(extra_user)
        db.session.commit()
        
    
    for title, time, loc, desc, image in zip(titles, times, locs, descs, images):
        
        duplicate_event = False
        for event in Event.query.all():
            if title == event.title:
                duplicate_event = True
        
        if duplicate_event == False:
            event = Event(title=title, date_posted=time, event_thumbnail=image, location=loc, description=desc, organizer_uuid=extra_user.uuid)
            db.session.add(event)
            db.session.commit()


def open_page(URL):

    driver = None
        
    if os.name == 'posix':
    
        #options = webdriver.ChromeOptions()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        #options.add_argument('headless')
        chrome_options.binary_location = '/opt/google/chrome/chrome'
        chrome_driver_binary = '/usr/local/bin/chromedriver'
        
        driver = webdriver.Chrome(chrome_driver_binary, chrome_options=chrome_options)
            
    
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        location = os.environ.get('WEB_CHROME')
    
        driver = webdriver.Chrome(location, chrome_options=options)
    

    driver.get(URL)
    r = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    return r
    
    
def combine_time(URL, event, link, times):
    
    combined_time = ''
    
    for time in times:
        combined_time += '{} '.format(event.find(time[1], class_=time[0]).text)    
        
    return combined_time
    
    
    
    
    
    
    

    
    
