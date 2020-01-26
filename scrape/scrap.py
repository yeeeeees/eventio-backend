from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import os

pages = {

    'eventim': {
        'URL': 'https://www.eventim.hr/hr/venues/split/city.html',
        'holder': {
            'type': 'a',
            'class': 'm-eventListItem'
        },
        'name': {
            'type': 'h3',
            'class': 'm-eventListItem__title'
        },
        'loc': {
            'type': 'span',
            'class': 'm-eventListItem__venue'
        },
        'time': {
            'type': 'span',
            'class': 'm-eventListItem__dateItem'
        },
        'img': {
            'link': 'https://www.eventim.hr',
            'type': 'img',
            'class': 'pageheader-bgimage'
        },
        'text': {
            'link': 'https://www.eventim.hr',
            'type': 'section',
            'class': 'Artist-section section clearfix'
        }
    },
    'adriticket': {
        'URL': 'https://adriaticket.com/',
        'holder': {
            'type': 'div',
            'class': 'col-md-6 col-sm-6 col-xs-12 one-event ng-scope'
        },
        'name': {
            'type': 'h4',
            'class': 'ng-binding'
        },
        'loc': {
            'type': 'div',
            'class': 'mjesto'
        },
        'time': {
            'type': 'div',
            'class': 'vrijeme'
        },
        'img': {
            'link': 'https://adriaticket.com',
            'type': 'div',
            'class': 'col-md-12 event-image '
        },
        'text': {
            'link': 'https://adriaticket.com',
            'type': 'div',
            'class': 'col-md-8'
        }
    }
}


class Event():
    def __init__(self, URL, HOLDER, NAME, LOC, TIME, IMG, TEXT):

        self.URL = URL
        self.HOLDER = HOLDER
        self.NAME = NAME
        self.LOC = LOC
        self.TIME = TIME
        self.IMG = IMG
        self.TEXT = TEXT
        self.name = []
        self.time = []
        self.loc = []
        self.r = open_page(self.URL)

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

            if event.get('href') is None:
                events.append(self.IMG[0] + event.a.get('href'))
            else:
                events.append(self.IMG[0] + event.get('href'))

        for event in events:

            r = open_page(event)
            soup = bs4(r, 'html.parser')

            image_holder = soup.find(self.IMG[1], class_=self.IMG[2])

            if image_holder.get('src') is None:
                image.append(image_holder.img.get('src'))
            else:
                image.append(image_holder.get('src'))

        return image

    def get_text(self):

        events = []
        text = []

        soup = bs4(self.r, 'html.parser')
        events_holder = soup.find_all(self.HOLDER[0], class_=self.HOLDER[1])

        for event in events_holder:

            if event.get('href') is None:
                events.append(self.TEXT[0] + event.a.get('href'))
            else:
                events.append(self.TEXT[0] + event.get('href'))

        for event in events:

            r = open_page(event)
            soup = bs4(r, 'html.parser')

            try:
                text_holder = soup.find(self.TEXT[1], class_=self.TEXT[2])
                text.append(text_holder.div.text)
            except AttributeError:
                text.append(None)

        return text


def open_page(URL):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    location = os.environ.get('WEB_CHROME')

    driver = webdriver.Chrome(location, chrome_options=options)
    driver.get(URL)

    r = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    return r


def main():

    for page in pages:
        page_event = Event(pages[page]['URL'],
                           (pages[page]['holder']['type'], pages[page]['holder']['class']),
                           (pages[page]['name']['type'], pages[page]['name']['class']),
                           (pages[page]['loc']['type'], pages[page]['loc']['class']),
                           (pages[page]['time']['type'], pages[page]['time']['class']),
                           (pages[page]['img']['link'], pages[page]['img']['type'], pages[page]['img']['class']),
                           (pages[page]['text']['link'], pages[page]['text']['type'], pages[page]['text']['class']))

        print(page_event.get_img())


if __name__ == "__main__":
    main()
