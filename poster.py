import configparser
import copy
import logging
import os
import random
import time

from selenium import webdriver

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONGRAGULATIONS_MSG_TEMPLATE = ["good luck bro!!!!!!!!",
                                "all the best!!!!!!!!!!!", "best of luck!!!!!!!!!!!!",
                                "hope u huat big big!!", "good luck bet within your means ah!",
                                "good luck 888!!!!!!!!!!", "best of luckkkkkkk!!!!!!!!!!"]


class ForumCrawler:

    def __init__(self, remote_session_id=""):
        self.driver_path = os.path.join(os.getcwd(), "chromedriver")

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver_options = options

        self.start_time = time.time()
        self.driver = None
        self.messages = []
        self.remote_session_id = remote_session_id

        config_data = configparser.ConfigParser()
        config_data.read('config.txt')
        self.username = config_data.get('webcredentials', 'username')
        self.password = config_data.get('webcredentials', 'password')
        self.homepage = config_data.get('webcredentials', 'homepage')

    def calculate_time(self):
        seconds_took = time.time() - self.start_time
        minutes_took = seconds_took / 60
        logger.info("Program took " + str(minutes_took) + " minutes")

    def start_browser(self):

        if self.remote_session_id:
            url = "http://127.0.0.1:4444/wd/hub"
            self.driver = webdriver.Remote(command_executor=url, desired_capabilities=self.driver_options.to_capabilities())
            self.driver.session_id = self.remote_session_id
        else:
            self.driver = webdriver.Chrome(
                self.driver_path, options=self.driver_options)
        self.driver.get(self.homepage)
        logger.info("Crawler going to homepage: ", self.homepage)

        agree_button = self.driver.find_element_by_xpath(
            "//input[@name='btnClose']")
        agree_button.click()
        logger.info("Agree button clicked")

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
        logger.info("Crawler sucessfully logged in")

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

        channel_links = ['https://forums.asianbookie.com/viewtopics.cfm?Forum=32', 'https://forums.asianbookie.com/viewtopics.cfm?Forum=33', 'https://forums.asianbookie.com/viewtopics.cfm?Forum=33', 'https://forums.asianbookie.com/viewtopics.cfm?Forum=34', 'https://forums.asianbookie.com/viewtopics.cfm?Forum=35', 'https://forums.asianbookie.com/viewtopics.cfm?Forum=36']

        for cl in channel_links:
            self.driver.get(cl)
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
                logger.info("One post...posted up!")

                self.driver.implicitly_wait(100)

                if(count % 10 == 0 and count != 0):
                    self.driver.quit()
                    time.sleep(600)
                    self.start_browser()
                    self.login()

        self.calculate_time()
        self.driver.quit()


if __name__ == "__main__":
    remote_session_id = ""
    fc = ForumCrawler(remote_session_id=remote_session_id)
    fc.run_crawler()
