import logging
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = logging.getLogger('seleniumlogger')



def start_browser():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', firefox_options=options)

    return driver


def get_twitter(driver, url):
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

            followers = a_div[1].text.replace(',', '').split(" ")[0]

        except NoSuchElementException:
            logger.info('[TWITTER] NoSuchElementException on %s' % url)
            followers = None
        finally:
            return followers


def init_driver_insta(driver, cookies):
    driver.get('https://www.instagram.com')
    time.sleep(2)
    try:
        accept = driver.find_elements_by_xpath("//button[contains(@class, 'aOOlW') and " +
                                               "contains(@class, 'bIiDR')]")
        accept[0].click()
        for cookie in cookies:
            driver.add_cookie(cookie)
    except (NoSuchElementException, IndexError):
        pass
    return driver


def get_insta(driver, url, cookies):
    if driver is not None:
        followers = None
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get(url)
        logger.info(url)
        time.sleep(2)
        try:
            followers = driver.find_elements_by_xpath("//span[contains(@class, 'g47SY')]")[1].text
        except NoSuchElementException:
            logger.info('[TWITTER] NoSuchElementException on %s' % url)
            followers = None
        finally:
            return followers

def connect_facebook(driver):
    email = "nepal75sess@gmail.com"
    password = "chocapic"
    url = "https://www.facebook.com/login"
    driver.get(url)
    time.sleep(4)
    driver.find_elements_by_xpath("//button[contains(@data-cookiebanner, 'accept_button')]")[0].click()
    email_div = driver.find_element_by_id("email")
    password_div = driver.find_element_by_id("pass")
    email_div.send_keys(email)
    password_div.send_keys(password)
    driver.find_element_by_id("loginbutton").click()
    time.sleep(2)

    return driver

def get_facebook(driver, url):
    followers = None
    url = "https://www.facebook.com/docgynecooffi"
    followers_url = url + '/folllowers'
    driver.get(url)
    logger.info(url)
    time.sleep(5)
    try:
        '''
        span_div = driver.find_elements_by_xpath("//span[contains(@class, 'd2edcug0') and " +
                                                 "contains(@class, 'hpfvmrgz') and " +
                                                 "contains(@class, 'qv66sw1b') and " +
                                                 "contains(@class, 'c1et5uql') and " +
                                                 "contains(@class, 'b0tq1wua') and " +
                                                 "contains(@class, 'a8c37x1j') and " +
                                                 "contains(@class, 'keod5gw0') and " +
                                                 "contains(@class, 'nxhoafnm') and " +
                                                 "contains(@class, 'aigsh9s9') and " +
                                                 "contains(@class, 'd9wwppkn') and " +
                                                 "contains(@class, 'fe6kdd0r') and " +
                                                 "contains(@class, 'mau55g9w') and " +
                                                 "contains(@class, 'c8b282yb') and " +
                                                 "contains(@class, 'hrzyx87i') and " +
                                                 "contains(@class, 'jq4qci2q') and " +
                                                 "contains(@class, 'a3bd9o3v') and " +
                                                 "contains(@class, 'knj5qynh') and " +
                                                 "contains(@class, 'oo9gr5id') and " +
                                                 "contains(@class, 'hzawbc8m')] ")
        '''
        span_div = driver.find_elements_by_xpath("//a[contains(@href, '_1nq8')]")

        if not span_div:
            divs = driver.find_elements_by_xpath("//div[contains(@class, '_4bl9')]")
            if not divs or divs[0].text == '':
                divs = driver.find_elements_by_xpath("//div[contains(@class, '_1nq8') and " +
                                                     "contains(@class, '_2ieq')]")
                if not divs:
                    raise NoSuchElementException
                followers = divs[0].text.split(' ')[2]

            followers = divs[3].text.split(' ')[0]
        else:
            followers = span_div[0].text.split(' ')[0]

    except NoSuchElementException:
        logger.info('[FACEBOOK] NoSuchElementException on %s' % url)
        followers = None
    finally:
        return followers

def exit_browser(driver):
    if driver is not None:
        driver.close()
