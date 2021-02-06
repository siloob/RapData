import logging
import requests

from data.models import RapGeniusTokens

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

    datas['facebook_name'] = json_response['response']['artist']['facebook_name']
    datas['instagram_name'] = json_response['response']['artist']['instagram_name']
    datas['twitter_name'] = json_response['response']['artist']['twitter_name']

    datas['genius_followers'] = json_response['response']['artist']['followers_count']
    datas['genius_image'] = json_response['response']['artist']['image_url']
    datas['genius_url'] = json_response['response']['artist']['url']

    return datas
        
