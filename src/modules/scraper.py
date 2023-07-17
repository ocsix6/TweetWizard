from modules.logger import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import random
import time

class Scraper:
    def __init__(self, url, mail, usr, psw):
        self.url = url
        options = Options()
        # Do not open the browser, run in background
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        # Suppress the "DevTools listening on ws://" message
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.mail = mail
        self.driver = webdriver.Chrome(chrome_options = options)
        self.login(mail, usr, psw)
        self.reject_cookies()

    def login(self, mail, username, password):
        with tqdm(total=100, desc=f"Opening {mail} session...", bar_format="\033[32m{desc}\033[0m |{bar}| {percentage:3.0f}%") as progress:
            self.driver.get(self.url)
            # Fill mail field
            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.NAME, "text")))
            
            self.driver.find_element('name','text').send_keys(mail+Keys.ENTER)
            progress.update(50)
            # Fill password field
            try:
                # Wait a maximum of 3 seconds for the element to be visible
                wait = WebDriverWait(self.driver, timeout=3, poll_frequency=1)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input [@autocomplete='current-password']")))

                self.driver.find_element(By.XPATH, "//input [@autocomplete='current-password']").send_keys(password)
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div").click()
            except (TimeoutException, NoSuchElementException):
                # Exception for the case when Twitter asks for username
                self.driver.find_element(By.XPATH, "//input [@inputmode='text' and @class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']").send_keys(username)
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div").click()
                
                # Wait a maximum of 10 seconds for the element to be visible
                wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input [@autocomplete='current-password']")))

                self.driver.find_element(By.XPATH, "//input [@autocomplete='current-password']").send_keys(password)
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div").click()
            progress.update(50)
            progress.set_description(f"\033[33m{mail}. Session opened\033[0m")

        # Save in log file that user has logged in
        logger.info(f'{self.mail} - Log in')

    def logout(self):
        with tqdm(total=100, desc=f"Closing {self.mail} session...", bar_format="\033[32m{desc}\033[0m |{bar}| {percentage:3.0f}%") as progress:
            self.go_to("https://twitter.com/logout")
            progress.update(50)

            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div [@role='button' and @data-testid='confirmationSheetConfirm']")))
            
            self.driver.find_element(By.XPATH, "//div [@role='button' and @data-testid='confirmationSheetConfirm']").click()
            progress.update(50)
            progress.set_description(f"\033[33m{self.mail}. Session closed\033[0m")

        logger.info(f'{self.mail} - Log out')

    def reject_cookies(self):
        # Wait a maximum of 4 seconds for the element to be visible
        try:
            wait = WebDriverWait(self.driver, timeout=4, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]")))
            
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]").click()
        except (TimeoutException, NoSuchElementException):
            pass
    
    def like_tweet(self, url):
        with tqdm(total=100, desc=f"Generating like with {self.mail}...", bar_format="\033[32m{desc}\033[0m |{bar}| {percentage:3.0f}%") as progress:
            if url != self.driver.current_url:
                self.go_to(url)
            progress.update(50)
            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div [@role='button' and @data-testid='like']")))
            
            self.driver.find_element(By.XPATH, "//div [@role='button' and @data-testid='like']").click()
            progress.update(50)
            progress.set_description(f"\033[33m{self.mail}. Liked tweet\033[0m")

        logger.info(f'{self.mail} - Liked tweet: {url}')

    def retweet(self, url):
        with tqdm(total=100, desc=f"Generating retweet with {self.mail}...", bar_format="\033[32m{desc}\033[0m |{bar}| {percentage:3.0f}%") as progress:
            if url != self.driver.current_url:
                self.go_to(url)
            progress.update(20)
            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div [@role='button' and @data-testid='retweet']")))
            
            self.driver.find_element(By.XPATH, "//div [@role='button' and @data-testid='retweet']").click()
            progress.update(40)
            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div")))
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div").click()
            progress.update(40)
            progress.set_description(f"\033[33m{self.mail}. Retweeted tweet\033[0m")

        logger.info(f'{self.mail} - Retweeted tweet: {url}')

    def comment_tweet(self, url, comment):
        with tqdm(total=100, desc=f"Generating like with {self.mail}...", bar_format="\033[32m{desc}\033[0m |{bar}| {percentage:3.0f}%") as progress:
            if url != self.driver.current_url:
                self.go_to(url)
            progress.update(25)
            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div [@role='button' and @data-testid='reply']")))
            
            self.driver.find_element(By.XPATH, "//div [@role='button' and @data-testid='reply']").click()
            progress.update(25)
            # Wait a maximum of 10 seconds for the element to be visible
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div [@role='textbox' and @data-testid='tweetTextarea_0']")))

            self.driver.find_element(By.XPATH, "//div [@role='textbox' and @data-testid='tweetTextarea_0']").send_keys(comment)
            progress.update(25)

            # Generate random number between 1 and 3
            system_random = random.SystemRandom()
            wait_time = system_random.randrange(1, 3)
            time.sleep(wait_time)
            self.driver.find_element(By.XPATH, "//div [@role='button' and @data-testid='tweetButton']").click()
            progress.update(25)
            progress.set_description(f"\033[33m{self.mail}. Commented tweet\033[0m")

        logger.info(f'{self.mail} - Commented: "{comment}" in tweet: {url}')
    
    def go_to(self, url):
        self.driver.get(url)
    
    def close(self):
        self.driver.close()