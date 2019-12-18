#!/usr/bin/python3

from __future__ import annotations
from colorama import Fore, init as color_init
from colorama.initialise import reset_all
from os import environ
from os.path import join
import re
from sys import platform
from subprocess import run
from city import fetch as fetch_city
from records import fetch_city_name_id, store_city_name_id
from weather import fetch as fetch_weather

'''
    If you're using this script from a certain directory for the very first time,
    make sure you choose 1 in main menu and create local database, holding City info.
    After that you may use any options as you intend.
    If you've already installed it, by executing install.py, then you're good to go.
'''


def __fetch_a_certain_city__(db_name):
    tmp = input(
        '[?]Search by\n\t1. CityName ( finds all possible matches )\n\t2. CityID\n>> ')
    resp = {}
    try:
        tmp = int(tmp)
    except ValueError as e:
        resp = {'error': str(e)}
        return resp
    if(tmp not in range(1, 3)):
        resp = {'error': 'bad input'}
        return resp
    if(tmp == 1):
        city_name = input('[?]Get me CityName >> ')
        if(not city_name):
            resp = {'error': 'bad input'}
            return resp
        resp = fetch_city_name_id(city_name=city_name, db_name=db_name)
        if(not resp or resp.get('status')):
            resp = {'error': 'found no record'}
    else:
        city_id = input('[?]Get me CityID >> ')
        if(not city_id):
            resp = {'error': 'bad input'}
            return resp
        resp = fetch_city_name_id(city_id=city_id, db_name=db_name)
        if(not resp or resp.get('status')):
            resp = {'error': 'found no record'}
    return resp


def __get_menu__() -> int:
    ch = input('[+]Main Menu:\n\t1. Fetch City Names\n\t2. Fetch a certain City\n\t3. Fetch Weather data of a City\n[?]Choose one >> ')
    try:
        ch = int(ch)
    except ValueError as e:
        print('[!]Error : {}'.format(str(e)))
        ch = -1
        return ch
    if ch not in range(1, 4):
        print('[!]Bad input')
        ch = -1
    return ch


def app():
    run('clear')
    print('[+]City Weather ::\n\n***Choose 1 from below list for first time use***\n')
    ch = __get_menu__()
    if(ch == -1):
        return
    if(ch == 1):
        resp = fetch_city()
        if(not resp.get('error')):
            print(
                '[+]Status after storing record : {}'.format(store_city_name_id(resp, db_name=db_name)))
            print('\n')
            for i, j in resp.items():
                print('\t{}\n'.format(i))
                for k in j:
                    for l, m in k.items():
                        print('\t\t\'{}\'  |  {}'.format(l, m))
                print('\n')
        else:
            print('[!]{} -> {}\n'.format('Error', resp.get('error', ':/')))
            resp = fetch_city_name_id()
            for i, j in resp.items():
                print('\t\t{}\t---\t{}'.format(i, j))
    elif(ch == 2):
        resp = __fetch_a_certain_city__()
        print('\n')
        for i, j in resp.items():
            print('\t{}\t---\t{}'.format(i, j))
        print('\n')
    else:
        resp = __fetch_a_certain_city__()
        print('\n')
        if(resp.get('error')):
            print('{}\n'.format(resp))
        else:
            if(len(resp.keys()) > 1):
                print('[+]Possible Matches found ...\n')
                for i, j in enumerate(resp.keys()):
                    print('\t{} -> {}'.format(i+1, resp.get(j)))
                tmp = input('\n[?]Choose one from above >> ')
                try:
                    tmp = int(tmp)
                except ValueError as e:
                    print('[!]Error : {}'.format(str(e)))
                    return
                if(tmp not in range(1, len(resp.keys())+1)):
                    print('[!]Bad input')
                    return
                resp = {list(resp.keys())[tmp-1]
                             : resp.get(list(resp.keys())[tmp-1])}
            else:
                print('[+]Match found :\n\t{}\n'.format(resp))
            print('[+]Fetching data ...\n')
            city_id = list(resp.keys())[0]
            weather = fetch_weather(city_id)
            if(weather.get('error')):
                print('{}\n'.format(weather))
                return
            print('[+]Weather Data :\n')
            pref_it = 'http://city.imd.gov.in/citywx/'
            color_init()
            for i, j in weather.get(city_id).items():
                if(i == 'past_24_hours_weather'):
                    print('\t{}{}{} :\n'.format(Fore.GREEN, ' '.join(
                        [x.capitalize() for x in i.split('_')]), Fore.RESET))
                    for k, l in j.items():
                        if(k.startswith('Departure from Normal(oC)')):
                            k = 'Departure from Normal(oC)'
                        print('\t\t{:<90} ---  {}{}{}'.format(k,
                                                              Fore.RED, l, Fore.RESET))
                    print('\n')
                elif(i == '7_days_forecast'):
                    print('\t{}{}{} :\n'.format(Fore.GREEN, ' '.join(
                        [x.capitalize() for x in i.split('_')]), Fore.RESET))
                    for k in j:
                        k[3] = Fore.MAGENTA+pref_it+k[3]+Fore.RESET
                        print('\t\t{} | {} | {} | {}'.format(*k))
                    print('\n')
                else:
                    print('\t{}{}{}\t---\t{}\n'.format(Fore.GREEN, ' '.join([x.capitalize(
                    ) for x in i.split('_')]), Fore.RESET, Fore.MAGENTA+pref_it+j+Fore.RESET))
            reset_all()
            print('[+]End\n')
    return


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
