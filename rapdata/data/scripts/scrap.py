import requests
import logging
import time
import re

from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.firefox.options import Options

scraplogger = logging.getLogger('scrapperlogger')

def get(url):    
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path='C:\\Users\\PETROU\\Documents\\dev\\geckodriver.exe', firefox_options=options)  
    browser.get(url)
    time.sleep(2)  
    print(browser.find('css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')) 
    browser.quit()

def get_twitter_datas(name):
    url = ('https://twitter.com/%s' % name)
    get(url)
    #scraplogger.info('[GET] %s' % url)
    #nb_followers = re.findall('followers_count&quot;:(.*),&quot;fr',rq.text)[0].replace(' ','')
    #return nb_followers

def get_instagram_datas(name):
    url = ('https://www.instagram.com/%s' % name)
    scraplogger.info(('[GET] %s' % url))
    rq = requests.get(url)
    print(rq.text)
    followers = re.findall('"edge_followed_by":{"count":(.*)}',rq.text)[0].split('}')[0]
    return int(followers)

def get_facebook_datas(name):
    url = ('https://www.facebook.com/%s' % name)
    scraplogger.info(('[GET] %s' % url))
    rq = requests.get(url)

    soup = BeautifulSoup(rq.text,'html.parser')
    likes = soup.find_all('span',attrs={'class':'_52id _50f5 _50f7'})
    likes = int(likes[0].text.split('m')[0].replace('\xa0','')) if likes else None
    
    return likes