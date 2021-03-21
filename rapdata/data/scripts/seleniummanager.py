import logging
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger('seleniumlogger')

driver = None

def start_browser():
    global driver
    if driver is None:
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='/home/nepal/Documents/dev/RapData/driver/geckodriver', firefox_options=options)

def get_twitter(url):
    global driver
    if driver is not None:
        followers = None
        driver.get(url)
        logger.info(url)
        time.sleep(2)
        try:
            a_div = driver.find_elements_by_xpath("//a[contains(@class, 'css-901oao') and " +
                                                "contains(@class, 'css-4rbku5') and " +
                                                "contains(@class, 'css-18t94o4') and " +
                                                "contains(@class, 'css-901oao') and " +
                                                "contains(@class, 'r-18jsvk2') and " +
                                                "contains(@class, 'r-1loqt21') and " +
                                                "contains(@class, 'r-1qd0xha') and " +
                                                "contains(@class, 'r-a023e6') and " +
                                                "contains(@class, 'r-16dba41') and " +
                                                "contains(@class, 'r-rjixqe') and " +
                                                "contains(@class, 'r-bcqeeo') and " +
                                                "contains(@class, 'r-qvutc0')] ")

            if not a_div:
                raise NoSuchElementException

            followers = a_div[1].text.replace(',','').split(" ")[0]

        except NoSuchElementException:
            logger.info('[TWITTER] NoSuchElementException on %s' % url)
            followers = None
        finally:
            return followers

def exit_browser():
    global driver
    if driver is not None:
        driver.close()
