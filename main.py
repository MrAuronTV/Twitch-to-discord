#!/usr/bin/env python3
import pickle
import requests
import json
import time
import urllib.request
from urllib import request
from urllib.error import HTTPError
from json import loads

WEBHOOK_URL = 'YOUR_WEBHOOK_URL' # Discord webhook url
PATH = 'YOUR_PATH' #Path where you stock clip id for doesnt spam discord

try:
    id = pickle.load(open("{}/twitch".format(PATH), "rb"))

except (OSError, IOError) as e:
    foo = 3
    pickle.dump(foo, open("{}/twitch".format(PATH), "wb"))
    

API_ENDPOINT = 'https://api.twitch.tv/helix/streams?user_login=<YOUR TWITCH USERNAME>'

#Create app https://dev.twitch.tv/console/apps
Client_ID = 'CLIENT_ID'
#Get twitch token https://id.twitch.tv/oauth2/authorize?client_id=CLIENT_APP_ID&redirect_uri=URI_APP&response_type=token
TOKEN = 'Bearer YOUR_TOKEN'

  
#data to be sent to api
head = {
"Authorization":  TOKEN,
'Client-ID' : Client_ID
}
#api call here
r = requests.get(url = API_ENDPOINT, headers = head)

GAME_ENDPOINT = 'https://api.twitch.tv/helix/games?id={0}'.format(loads(r.text)['data'][0]['game_id'])

g = requests.get(url = GAME_ENDPOINT, headers = head)

# La payload tag follower <@&405395588763353089>
payload = {
    'username':"Botname",
    'content': "message",
    'avatar_url':"avatar url",
    'embeds': [
        {
            'title': loads(r.text)['data'][0]['title'],  # Le titre de la carte
            'description': 'description',  # Le corps de la carte
            'url': 'https://www.twitch.tv/mraurontv',  # Si vous voulez faire un lien
            "color": 6570404,
	    'author': {'name': 'author'},  # Pourquoi pas mettre des auteurs ?
            'timestamp':  loads(r.text)['data'][0]['started_at'],
            "image": {"url": 'https://static-cdn.jtvnw.net/previews-ttv/live_user_{}-1280x720.jpg?rnd={}'.format(loads(r.text)['data'][0]['user_login'],int(time.time()))}, 
	    "fields": [
      		{
       		 "name": "Game",
	        "value": loads(g.text)['data'][0]['name'],
		"inline": True,
      		},
      		{
        	"name": "Viewers",
        	"value": loads(r.text)["data"][0]['viewer_count'],
       		"inline" : True,
		}
            ]
        },
    ]
}

# Les paramètres d'en-tête de la requête
headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

# Enfin on construit notre requête
req = request.Request(url=WEBHOOK_URL,
                      data=json.dumps(payload).encode('utf-8'),
                      headers=headers,
                      method='POST')

if loads(r.text)['data'][0]['user_id']:
    if loads(r.text)['data'][0]['id'] != id:
        response = request.urlopen(req)

with open('{}/twitch'.format(PATH), 'wb') as f:
    pickle.dump(loads(r.text)['data'][0]['id'], f)