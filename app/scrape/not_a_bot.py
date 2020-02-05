from selenium import webdriver
import os
import time


class Not_a_IG_bot:

    def __init__(self, username, password):

        self.username = username
        self.password = password

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.driver = webdriver.Chrome(os.environ.get('WEB_CHROME'),
                                       chrome_options=options)
        self.URL = 'https://www.instagram.com'

        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.URL))
        time.sleep(1)

        username_input = self.driver.find_element_by_name("username")
        password_input = self.driver.find_element_by_name("password")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()
        time.sleep(2)

    def nav_user(self, user):
        self.driver.get('{}/{}'.format(self.URL, user))

    def open_post(self, user):
        self.nav_user(user)
        time.sleep(2)

        post = self.driver.find_element_by_class_name('eLAPa')
        post.click()

    def get_text(self, user):
        self.open_post(user)
        time.sleep(2)

        text = self.driver.find_element_by_class_name('C4VMK').text
        print(text)

    def get_img(self, user):
        self.open_post(user)
        time.sleep(2)

        img = self.driver.find_element_by_class_name('FFVAD')
        print(img.get_attribute('src'))


if __name__ == "__main__":
    ig_bot = Not_a_IG_bot(os.environ.get('BOT_USER'),
                          os.environ.get('BOT_PASS'))

    ig_bot.get_text('medialunes')
    ig_bot.get_img('medialunes')
