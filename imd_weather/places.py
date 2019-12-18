#!/usr/bin/python3

from __future__ import annotations
from requests import get
from re import compile as reg_compile
from bs4 import BeautifulSoup
from typing import Dict, List
from json import dump, load
from .state import State
from .station import Station


class Places(object):
    def __init__(self, states: List[State]):
        self.states = states

    @staticmethod
    def fromJSON(source: str) -> Places:
        try:
            with open(source, mode='r') as fd:
                return Places([State.fromJSON(v, k) for k, v in load(fd).items()])
        except Exception:
            return Places([])

    def toJSON(self) -> Dict[str, List[Dict[str, str]]]:
        return dict([(i.name, i.toJSON()) for i in self.states])

    @staticmethod
    def _parse(content: str) -> Places:
        '''
            Parses HTML, using BeautifulSoup.
        '''
        placesObj = Places([])
        state_name = reg_compile(r'^(##)$')
        station_name = reg_compile(r'^(city_weather.php\?id=[\d]{1,5})$')
        root = BeautifulSoup(content, features='lxml')
        currentState = None
        for i in root.findAll('a'):
            if state_name.match(i.get('href')):
                currentState = State(i.getText(), [])
                placesObj.states.append(currentState)
            if station_name.match(i.get('href')):
                currentState.stations.append(
                    Station(i.getText(), currentState.name, i.get('href')))
        return placesObj

    @staticmethod
    def _get(base_url: str) -> Places:
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
        placesObj = Places._parse(resp.content) if resp.ok else None
        resp.close()
        return placesObj

    @staticmethod
    def fetch(base_url: str = 'http://city.imd.gov.in/citywx/menu.php') -> Places:
        '''
            Fetches city names, corresponding url and city id from IMD website.
        '''
        return Places._get(base_url)


'''
def writeAsJSON(data: Dict[str, Dict[str, str]], sink: str):
    
        Writes collected city data i.e. corresponding state names,
        city names & urls(where weather data can be requested),
        into a JSON file
    
    with open(sink, mode='w') as fd:
        dump(data, fd, ensure_ascii=False, indent=4)
'''

if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
