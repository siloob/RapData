import requests
import logging
import time
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

def get_insta_cookies():
    url_csrf = 'https://www.instagram.com/accounts/login/'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.get(url_csrf, headers=headers)
    if r.status_code != 200:
        return
    csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
    USERNAME = 'rapdatafr'
    MDP = 'chocapic'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    timestamp = int(time.time())
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://www.instagram.com/accounts/login/",
        'X-CSRFToken': csrf
    }
    payload = {
        'username':USERNAME,
        'enc_password':'#PWD_INSTAGRAM_BROWSER:0:%s:%s' % (timestamp, MDP),
        'queryParams':{},
        'optIntoOneTap': 'false',
    }

    r = requests.post(url=url_login,data=payload, headers=headers)
    if r.status_code == 200:
        user_id = r.json()['userId']
        session_id = r.headers['Set-Cookie'].split('sessionid=')[1].split(';')[0]
        return [
            {
                'name':'ds_user_id',
                'value':user_id
            },
            {
                'name':'sessionid',
                'value':session_id
            },
            {
                'name':'csrftoken',
                'value':csrf
            },
            {
                'name':'rur',
                'value':'VLL'
            },
            {
                'name':'ig_cb',
                'value':'2'
            }
        ]

def get_instagram_datas(name, cookies):
    url = ('https://www.instagram.com/%s/' % name)
    followers = seleniummanager.get_insta(url, cookies)
    if followers is None:
        return None
    if 'm' in followers:
        numbers = followers.replace('m','')
        if '.' not in numbers:
            followers = int(numbers)*1000000
        else:
            numbers = numbers.split('.')
            followers = int(numbers[0])*1000000 + int(numbers[1])*100000
    elif 'k' in followers:
        numbers = followers.replace('k','')
        if '.' not in numbers:
            followers = int(numbers)*1000
        else:
            numbers = numbers.split('.')
            followers = int(numbers[0])*1000 + int(numbers[1])*100
    else:
        numbers = followers.replace(',','')
        followers=int(numbers)
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