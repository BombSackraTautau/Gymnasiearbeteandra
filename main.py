#!/usr/bin/env python3
import json
import html
import requests
import datetime
import locale
import feedparser
from time import time, sleep
from flask import Flask, render_template, Markup
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

dt = datetime.datetime.now()

#SLbuss [Avgång från Huddinge Sjukhus]

headers = {
    'authority': 'webcloud.sl.se',
    'accept': '*/*',
    'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://sl.se',
    'referer': 'https://sl.se/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

params = {
    'mode': 'departures',
    'origPlaceId': 'QT0xQE89SHVkZGluZ2Ugc2p1a2h1cyAoSHVkZGluZ2UpQFg9MTc5Mzc1NDNAWT01OTIyMjI2NUBVPTc0QEw9MzAwMTA3MDAwQEI9MUBwPTE2NzA5ODY4MTBA',
    'origSiteId': '7000',
    'desiredResults': '10',
    'origName': 'Huddinge sjukhus (Huddinge)',
}

resp = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers,verify=False)
#print(response.text)

SLbuss = []
for t in resp.json():
    params = {
        'mot': t['destination'],
        'linje': t['transport']['line'],
        'om': t['time']['displayTime'],
        'stop': t['track']
    }
    #print(params)


try: 
    for s in resp.json():
        p = f"Buss {s['transport']['line']} mot {s['destination']} om: {s['time']['displayTime']} från STOP: {s['track']}"
        print(p)
        
        SLbuss.append(p)
except:
    print("error")
pass




#SLpendel [Avgång från Flemingsberg Station]
headers = {
    'authority': 'webcloud.sl.se',
    'accept': '*/*',
    'accept-language': 'sv,en-US;q=0.9,en;q=0.8',
    'origin': 'https://sl.se',
    'referer': 'https://sl.se/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
}

params = {
    'mode': 'departures',
    'origPlaceId': 'QT0xQE89RmxlbWluZ3NiZXJncyBzdGF0aW9uIChIdWRkaW5nZSlAWD0xNzk0Nzk4OEBZPTU5MjE5MjM2QFU9NzRATD0zMDAxMDcwMDZAQj0xQHA9MTY3MzQ5MjQyMEA=',
    'origSiteId': '7006',
    'desiredResults': '3',
    'origName': 'Flemingsbergs station (Huddinge)',
}

response = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers, verify=False)
#print(response.text)

SLpendel = []
for o in response.json():
    params = {
        'linje': o['transport']['line'],
        'mot': o['destination'],
        'om': o['time']['displayTime'],
        'transportType': o['transport']['transportType'],
        'spår': o['track']
    }
    for key, value in params.items():
        if key == "transportType" and value == "Train":
            z = f"Pendel linje {params['linje']} mot {params['mot']} om: {params['om']} från spår: {params['spår']}"
            print(z)
            SLpendel.append(z)

SLpendel = SLpendel

@app.route('/sl/')
def sl():
    return render_template('slappen.html', SLbuss=SLbuss, SLpendel=SLpendel)

@app.route('/hemma/')
def hemma():
    return render_template('index.html')

@app.route('/vader/')
def vader():
    return render_template('stockholmsvader.html')
    
@app.route('/vaderappen/')
def vaderappen():
    return render_template('vaderappen.html')

@app.route('/spel/')
def spel():
    return render_template('spel.html')

@app.route('/film/')
def film():
    return render_template('film.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)