import requests
from selenium import webdriver 
from bs4 import BeautifulSoup as bs4
import os
pages = {
    
    'eventim':{
        'URL':'https://www.eventim.hr/hr/venues/split/city.html',
        'holder':('a', 'm-eventListItem'),
        'name': ('h3', 'm-eventListItem__title'),
        'loc': ('span', 'm-eventListItem__venue'),
        'time': ('span', 'm-eventListItem__dateItem'),
        'img': ('https://www.eventim.hr', 'img', 'pageheader-bgimage')
    },

    'adriaticket':{
        'URL':'https://adriaticket.com/',
        'holder':('div', 'col-md-6 col-sm-6 col-xs-12 one-event ng-scope'),
        'name': ('h4', 'ng-binding'),
        'loc': ('div', 'mjesto'),
        'time': ('div', 'vrijeme'),
        'img': ('https://adriaticket.com', 'div', 'col-md-12 event-image ')
    }
}


class Event():
    def __init__(self, URL, HOLDER, NAME, LOC, TIME, IMG):
        
        self.URL = URL
        self.HOLDER = HOLDER
        self.NAME = NAME
        self.LOC = LOC
        self.TIME = TIME
        self.IMG = IMG
        self.name = []
        self.time = []
        self.loc = []

        self.r = open_page(URL)
        
        soup = bs4(self.r, 'html.parser')     
        events_holder = soup.find_all(HOLDER[0], class_=HOLDER[1])

        for event in events_holder:

            name_holder = event.find(NAME[0], class_=NAME[1]).text  
            self.name.append(name_holder) 

            loc_holder = event.find(LOC[0], class_=LOC[1]).text    
            self.loc.append(loc_holder)

            time_holder = event.find(TIME[0], class_=TIME[1]).text    
            self.time.append(time_holder)

    def get_img(self):

        events = []
        image = []

        soup = bs4(self.r, 'html.parser')
        events_holder = soup.find_all(self.HOLDER[0], class_=self.HOLDER[1])
      
        for event in events_holder:
            
            if event.get('href') == None:
                events.append(self.IMG[0] + event.a.get('href'))
            else:
                events.append(self.IMG[0] + event.get('href'))
            
      
        for event in events:

            r = open_page(event)

            soup = bs4(r, 'html.parser')

            image_holder = soup.find(self.IMG[1], class_=self.IMG[2])
            
            if image_holder.get('src') == None:
                image.append(image_holder.img.get('src'))
            else:
                image.append(image_holder.get('src'))
           
        return image


def open_page(URL):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    location = os.environ.get("WEBDRIVER_LOCATION")
    driver = webdriver.Chrome(location, chrome_options=options)
    driver.get(URL)
    
    r = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    
    return r

def main():

    for page in pages:
        eventim =   Event(pages[page]['URL'],
                    pages[page]['holder'], 
                    pages[page]['name'], 
                    pages[page]['loc'], 
                    pages[page]['time'],
                    pages[page]['img'])
    
        print(eventim.get_img())

if __name__ == "__main__":
    main()    