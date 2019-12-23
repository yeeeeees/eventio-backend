import requests
from selenium import webdriver 
from bs4 import BeautifulSoup as bs4

pages = {
    
    'eventim':{
        'URL':'https://www.eventim.hr/hr/venues/split/city.html',
        'holder':('a', 'm-eventListItem'),
        'name': ('h3', 'm-eventListItem__title'),
        'loc': ('span', 'm-eventListItem__venue'),
        'time': ('span', 'm-eventListItem__dateItem')
    },

    'adriaticket':{
        'URL':'https://adriaticket.com/',
        'holder':('div', 'col-md-6 col-sm-6 col-xs-12 one-event ng-scope'),
        'name': ('h4', 'ng-binding'),
        'loc': ('div', 'mjesto'),
        'time': ('div', 'vrijeme')
    }
}


class Event():
    def __init__(self, URL, HOLDER, NAME, LOC, TIME):
        
        self.URL = URL
        self.HOLDER = HOLDER
        self.NAME = NAME
        self.LOC = LOC
        self.TIME = TIME
        self.name = []
        self.time = []
        self.loc = []

        driver = webdriver.Chrome('C:/Users/PC/Downloads/chromedriver_win32/chromedriver.exe')
        driver.get(self.URL)

        # r = requests.get(URL) 
        r = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()
        
        soup = bs4(r, 'html.parser')     
        events_holder = soup.find_all(HOLDER[0],{'class':HOLDER[1]})

        for event in events_holder:

            name_holder = event.find(NAME[0], class_=NAME[1]).text  
            self.name.append(name_holder) 

            loc_holder = event.find(LOC[0], class_=LOC[1]).text    
            self.loc.append(loc_holder)

            time_holder = event.find(TIME[0], class_=TIME[1]).text    
            self.time.append(time_holder)

    def get_img(self):
        pass

def main():

    for page in pages:
        eventim =   Event(pages[page]['URL'],
                    pages[page]['holder'], 
                    pages[page]['name'], 
                    pages[page]['loc'], 
                    pages[page]['time'])
    
        print(eventim.time)

if __name__ == "__main__":
    main()    