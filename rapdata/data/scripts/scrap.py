import requests
import logging
import re

from bs4 import BeautifulSoup
import data.scripts.seleniummanager as seleniummanager

scraplogger = logging.getLogger('scrapperlogger')

def get_twitter_datas(name):
    url = ('https://twitter.com/%s' % name)
    followers = seleniummanager.get_twitter(url)
    if followers is None:
        return None
    if 'M' in followers:
        numbers = followers.replace('M','')
        if '.' not in numbers:
            followers = int(numbers)*1000000
        else:
            numbers = numbers.split('.')
            followers = int(numbers[0])*1000000 + int(numbers[1])*100000
    elif 'K' in followers:
        numbers = followers.replace('K','')
        if '.' not in numbers:
            followers = int(numbers)*100000
        else:
            numbers = numbers.split('.')
            followers = int(numbers[0])*100000 + int(numbers[1])*10000

    return int(followers)

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
    print(url)
    rq = requests.get(url)

    soup = BeautifulSoup(rq.text,'html.parser')
    likes = soup.find_all('span',attrs={'class':'_52id _50f5 _50f7'})
    likes = int(likes[0].text.split('m')[0].replace('\xa0','')) if likes else None
    
    if likes is None:
        url_followers = url+'/followers'
        likes = soup.find_all('a',attrs={'href': url_followers})
        '''
        print('followers')
        print(url_followers)
        print(likes)
        '''

    print(likes)
    return likes