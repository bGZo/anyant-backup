#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" Unstar all the starred items in the feed and backup.
"""

__author__      = "bGZo"
__update__      = "220520"
__version__     = "0.0.2"

import os.path
import json
import requests
import argparse

def init(loginUrl, data):
    if os.path.isfile('./data/config.json'):
        print('config.json exists.')
        f=open('data/config.json', 'r')
        config = json.load(f)
        header = config['header']
        f.close()

    else:
        print('config not exists!')

        header={
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
            # 'cookie': ''
            # 'x-csrftoken': ''
        }

        r = requests.post(loginUrl, headers=header, data=data)
        if r.status_code == 200:
            print('login success.')
        else:
            print('login failed!')
            exit()

        c = requests.utils.dict_from_cookiejar(r.cookies)
        header['cookie'] = 'csrftoken='+ c['csrftoken'] +'; sessionid='+ c['sessionid']
        header['x-csrftoken'] = c['csrftoken']
        backup={
            'header': header
            #'data': data
        }
        f = open('./data/config.json', 'w')
        f.write(json.dumps(backup, ensure_ascii=False)) 
        # NOTE: ' to ", via:https://wxnacy.com/2020/05/01/python-print-dict-double-quotation-marks/
        f.close()
        print('config.json created.')
    return header

def unfav_and_backup(header, favUrl):
    fav = requests.get(favUrl, headers=header) ## don't need x-cookie

    for i in fav.json()['storys']:
        tmp = str(i['feed']['id']) + '-' + str(i['offset'])
        favUrl='https://rss.anyant.com/api/v1/story/' + tmp + '/favorited'
        favR = requests.put(favUrl, headers=header, json={'is_favorited':'false'})
        if favR.status_code == 200:
            print(favR.json()['title'], 'unfav success.')
        else:
            print('unfav failed!', favR.text)
            exit()

    f=open('./data/backup.json', 'a')
    f.write(json.dumps(fav.json(), ensure_ascii=False))
    f.close()
    print('backup success.')

def main(data):
    loginUrl = 'https://rss.anyant.com/api/v1/user/login/'
    favUrl = 'https://rss.anyant.com/api/v1/story/favorited'

    header = init(loginUrl, data)
    unfav_and_backup(header, favUrl)

if __name__=='__main__':
    parser =argparse.ArgumentParser(description='Anyant Script.')
    parser.add_argument('account', metavar='account', type=str,
                    help='input your account')
    parser.add_argument('-p','-password', dest='password',type=str,
                    help='password')
    args = parser.parse_args()

    account = args.account
    password = args.password
    data={
        'account': account,
        'password': password
    }
    main(data)
