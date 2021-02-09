import logging
import requests

apilogger = logging.getLogger("apilogger")

URL = "https://api.genius.com"

def get_id(token, name):
    headers = {'Authorization': 'Bearer ' + token}
    url = ("%s/search?q=%s" % (URL, name))
    rq = requests.get(url, headers=headers)
    apilogger.info('[GET] %s' % url)

    json_response = rq.json()
    for hit in json_response['response']['hits']:
        genius_name =  hit['result']['primary_artist']['name']
        if genius_name.upper().replace(' ','') == name.upper().replace(' ',''):
            return hit['result']['primary_artist']['id']
    
    return None

def get_data(token, id):
    headers = {'Authorization': 'Bearer ' + token}
    url = ("%s/artists/%s" % (URL, id))
    rq = requests.get(url, headers=headers)
    apilogger.info('[GET] %s' % url)

    json_response = rq.json()
    datas= dict()

    fb = json_response['response']['artist']['facebook_name']
    insta = json_response['response']['artist']['instagram_name']
    twi = json_response['response']['artist']['twitter_name']

    datas['facebook_name'] = fb.split('?')[0] if fb and '?' in fb else fb
    datas['instagram_name'] = insta.split('?')[0] if insta in '?' in insta else insta
    datas['twitter_name'] = twi.split('?')[0] if twi and '?' in twi else twi

    datas['genius_followers'] = json_response['response']['artist']['followers_count']
    datas['genius_image'] = json_response['response']['artist']['image_url']
    datas['genius_url'] = json_response['response']['artist']['url']

    return datas
        
