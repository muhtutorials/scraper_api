import time

from fake_useragent import UserAgent
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from .utils import extract_asin, extract_price


# fake_useragent library has a bug
# https://stackoverflow.com/questions/68772211/fake-useragent-module-not-connecting-properly-indexerror-list-index-out-of-ra
def get_user_agent():
    return UserAgent(verify_ssl=False).random


class Scraper:
    url = None
    endless_scroll = False
    endless_scroll_time = 5
    driver = None
    html_obj = None

    def __init__(self, url, endless_scroll=False, endless_scroll_time=5):
        self.url = url
        self.endless_scroll = endless_scroll
        self.endless_scroll_time = endless_scroll_time

    def get_driver(self):
        if self.driver is None:
            user_agent = 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
            options = Options()
            # "--headless" argument won't open browser
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Remote('http://selenium-hub:4444/wd/hub', DesiredCapabilities.CHROME, options=options)
            self.driver = driver
        return self.driver

    def perform_endless_scroll(self, driver=None):
        if driver is None:
            return

        if self.endless_scroll:
            current_height = driver.execute_script('return document.body.scrollHeight')
            while True:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(self.endless_scroll_time)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if current_height == new_height:
                    break
                current_height = new_height
        return

    def get_page(self):
        driver = self.get_driver()
        driver.get(self.url)
        if self.endless_scroll:
            self.perform_endless_scroll(driver=driver)
        else:
            time.sleep(10)
        return driver.page_source

    def get_html_obj(self):
        if self.html_obj is None:
            html_str = self.get_page()
            self.html_obj = HTML(html=html_str)
        return self.html_obj

    def extract_element_text(self, element_id):
        html_obj = self.get_html_obj()
        element = html_obj.find(element_id, first=True)
        if not element:
            return ''
        return element.text

    def scrape_data(self):
        asin = extract_asin(self.url)
        title = self.extract_element_text('#productTitle')
        price = extract_price(self.extract_element_text('.a-price-whole'))
        return {
            'url': self.url,
            'asin': asin,
            'title': title,
            'price': price
        }
