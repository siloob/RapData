import hmac
import base64
import logging
import hashlib
import requests
import urllib.parse
from xml.etree import ElementTree

from data.models import Artist

apilogger = logging.getLogger("apilogger")

def sign(request, consumer_secret, token_secret = "", http_methode = 'GET'):
    a = request.split('?')
    host_uri = a[0]
    params = "a"
    if len(a) > 1:
        params = a[1]
    params = params.split('&')
    params = sorted(params)
    encoded_params = '&'.join(params)

    base = urllib.parse.quote(http_methode,'').replace('%7E','~').replace('+',' ') + '&'
    base += urllib.parse.quote(host_uri,'').replace('%7E','~').replace('+',' ') + '&'
    base += urllib.parse.quote(encoded_params,'').replace('%7E','~').replace('+',' ')

    hmac_key = urllib.parse.quote(consumer_secret,'').replace('%7E','~').replace('+',' ') + '&'
    if consumer_secret != "":
        hmac_key += urllib.parse.quote(token_secret,'').replace('%7E','~').replace('+',' ')

    oauth_signature = base64.b64encode(hmac.new(bytes(hmac_key,'utf-8'),base.encode('utf-8'),hashlib.sha1).digest())
    request += '&' if '?' in request else '?'
    request += 'oauth_signature=' + urllib.parse.quote(oauth_signature,'')
    if request[-3:] == "%0A":
        request = request[:-3]
    return request

def init_tokens(consumer_key, consumer_secret):
    url = "http://api.music-story.com/oauth/request_token?oauth_consumer_key=" + consumer_key
    url_signed = sign(url,consumer_secret)
    apilogger.info('[GET] %s' % url)
    rq = requests.get(url_signed)

    tree = ElementTree.fromstring(rq.content)
    data = tree.find('data')
    token = data.find('token').text
    token_secret = data.find('token_secret').text

    return CONSUMER_KEY, CONSUMER_SECRET, token, token_secret

def get_artists(consumer_secret, token, token_secret):
    artists = []
    url = "http://api.music-story.com/fr/genre/190/artists?oauth_token=" + token
    url = sign(url,consumer_secret,token_secret)
    apilogger.info('[GET] %s' % url)
    rq = requests.get(url)

    root = ElementTree.fromstring(rq.content)
    nbPages = root.find('pageCount').text
    for name,id in zip(root.iter('name'),root.iter('id')):
        artists.append((name.text, id.text))

    '''
    for i in range(1, int(nbPages)):
        url = "http://api.music-story.com/fr/genre/190/artists?oauth_token=" + token + "&page=" + str(i)
        url = sign(url,CONSUMER_SECRET,token_secret)
        apilogger.info('[REQUEST] %s' % url)
        rq = requests.get(url)

        root = ElementTree.fromstring(rq.content)
        for name,id in zip(root.iter('name'),root.iter('id')):
            ar = Artist(name.text,id.text)
            list_name_artist.append(ar)
    '''

    return artists
