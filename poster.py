import configparser
import copy
import os
import random
import time

from selenium import webdriver

CONGRAGULATIONS_MSG_TEMPLATE = ["good luck bro!!!!!!!!",
                                "all the best!!!!!!!!!!!", "best of luck!!!!!!!!!!!!",
                                "hope u huat big big!!", "good luck bet within your means ah!",
                                "good luck 888!!!!!!!!!!", "best of luckkkkkkk!!!!!!!!!!"]


class Forum_Crawler:

    def __init__(self):
        self.driver_path = os.path.join(os.getcwd(), "chromedriver")

        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        self.driver_options = options

        self.start_time = time.time()
        self.driver = None
        self.messages = []

        config_data = configparser.ConfigParser()
        config_data.read('config.txt')
        self.username = config_data.get('webcredentials', 'username')
        self.password = config_data.get('webcredentials', 'password')
        self.homepage = config_data.get('webcredentials', 'homepage')

    def calculate_time(self):
        seconds_took = time.time() - self.start_time
        minutes_took = seconds_took / 60
        print("Program took " + str(minutes_took) + " minutes")

    def start_browser(self):
        self.driver = webdriver.Chrome(
            self.driver_path, chrome_options=self.driver_options)
        self.driver.get(self.homepage)
        agree_button = self.driver.find_element_by_xpath(
            "//input[@name='btnClose']")
        agree_button.click()

    def login(self):
        login_link = self.driver.find_element_by_xpath(
            "//a[@href='//forums.asianbookie.com/login.cfm']")
        login_link.click()
        username_input = self.driver.find_element_by_xpath(
            "//input[@name='Username']")
        username_input.send_keys(self.username)

        password_input = self.driver.find_element_by_xpath(
            "//input[@name='Password']")
        password_input.send_keys(self.password)

        self.driver.implicitly_wait(30)
        login_button = self.driver.find_element_by_xpath(
            "//input[@name='Login']")
        login_button.click()
        self.driver.implicitly_wait(30)

    def get_post_titles(self):

        # currently only gets the first channel
        channel_links = self.driver.find_element_by_xpath(
            "//tr[@bgcolor='#336699']//a")
        channel_links.click()

        pt = self.driver.find_elements_by_xpath(
            "//tr[@bgcolor='#336699']//td[@valign='top']/b")
        return pt

    def get_individual_post_links(self):
        ipl = []

        post_titles = self.get_post_titles()

        for title in post_titles:
            if(title.text is None):
                continue
            else:

                if("Note" in title.text or "Sticky" in title.text):
                    continue

                #. signifies xpath relative to current node
                title_link = title.find_elements_by_xpath(
                    ".//a[@class='topics']")
                for t in title_link:
                    if(t.get_attribute('href') not in ipl):
                        ipl.append(t.get_attribute('href'))
        return ipl

    def generate_messages(self):
        messages = copy.deepcopy(CONGRAGULATIONS_MSG_TEMPLATE)
        random.shuffle(messages)
        self.messages = messages

    def run_crawler(self):
        self.start_browser()
        self.login()
        individual_post_links = self.get_individual_post_links()

        for count, ipl in enumerate(individual_post_links):
            # get post id
            forum_thread_suffix = ipl.split("?")[1]
            post_reply_url = "https://forums.asianbookie.com/replytotopic.cfm?" + \
                forum_thread_suffix + "&basic=1"
            self.driver.get(post_reply_url)

            # find list of users in current page and make sure there is no
            # repeated posts
            user_list = [x.text for x in self.driver.find_elements_by_xpath(
                "//tr[@bgcolor='##F9f9f9']//b")]
            if(self.username in user_list):
                continue

            # check if message list is empty
            if(not self.messages):
                self.generate_messages()

            text_box = self.driver.find_element_by_xpath(
                "//textarea[@id='editor2']")
            text_box.click()
            text_box.send_keys(self.messages.pop())

            submit_reply_button = self.driver.find_element_by_xpath(
                "//input[@name='InsertMessage']")
            submit_reply_button.click()
            self.driver.implicitly_wait(100)

            if(count % 10 == 0 and count != 0):
                self.driver.quit()
                time.sleep(600)
                self.start_browser()
                self.login()

        self.calculate_time()
        self.driver.quit()


if __name__ == "__main__":
    fc = Forum_Crawler()
    fc.run_crawler()
