#!/usr/bin/python3

from __future__ import annotations
from requests import get
from re import compile as reg_compile
from bs4 import BeautifulSoup
from typing import Dict
from json import dump


def _parse(content: str) -> Dict[str, Dict[str, str]]:
    '''
        Parsing of html page is done here, using BeautifulSoup.
    '''
    parsed = {}
    state_name = reg_compile(r'^(##)$')
    station_name = reg_compile(r'^(city_weather.php\?id=[\d]{1,5})$')
    root = BeautifulSoup(content, features='lxml')
    currentState = None
    for i in root.findAll('a'):
        if state_name.match(i.get('href')):
            currentState = i.getText()
            parsed[currentState] = {}
        if station_name.match(i.get('href')):
            parsed.get(currentState).update({i.getText(): i.get('href')})
    return parsed


def _get(base_url: str) -> Dict[str, Dict[str, str]]:
    '''
        Performs GET request at provided url and asks parser to do parsing
    '''
    resp = get(base_url,
               headers={
                   'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/71.0'
               })
    content = _parse(resp.content) if resp.ok else None
    resp.close()
    return content


def fetch(base_url: str = 'http://city.imd.gov.in/citywx/menu.php') -> Dict[str, Dict[str, str]]:
    '''
        Simply fetches city names, corresponding url and city id from IMD website,
        parses them and returns a python dict.
    '''
    return _get(base_url)


def writeAsJSON(data: Dict[str, Dict[str, str]], sink: str):
    '''
        Writes collected city data i.e. corresponding state names,
        city names & urls ( where weather data can be requested ),
        into a JSON file
    '''
    with open(sink, mode='w') as fd:
        dump(data, fd, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
