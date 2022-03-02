#!/usr/bin/python3
# author: bGZoCg
# update: 220212
# description: unstar all the starred items in the  feed
# requirement.txt
    # requests

import os.path
import json
import requests
import argparse

from datetime import date

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
        backup={'header': header}
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

    file = str(date.today())+'.json'
    f=open('./data/'+file, 'w')
    f.write(json.dumps(fav.json(), ensure_ascii=False))
    f.close()
    print('backup success.')
    return file

def update_index(file):
    f=open('./data/'+file, 'r')
    favs = json.load(f)['storys']
    f.close()

    f=open('./index.md', 'a')
    for i in favs:
        tmp = '| ' + i['title'] + ' | [jmp](' + i['link'] + ') | [jmp](' + \
        'https://rss.anyant.com/story?feed=' + \
        i['feed']['id'] + '&offset=' + str(i['offset']) + ') |\n'
        f.write(tmp)
    f.close()

def main(data):
    loginUrl = 'https://rss.anyant.com/api/v1/user/login/'
    favUrl = 'https://rss.anyant.com/api/v1/story/favorited'

    header = init(loginUrl, data)
    file = unfav_and_backup(header, favUrl)
    update_index(file)

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
