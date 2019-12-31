#!/usr/bin/python3

from __future__ import annotations
from requests import get
from re import compile as reg_compile
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple
from json import dump, load
from .state import State
from .station import Station
from urllib.parse import urljoin
from functools import reduce


class Places(object):
    def __init__(self, states: List[State]):
        self.states = states

    def _push(self, low: int, high: int, name: str) -> int:
        if low > high:
            return 0
        elif low == high:
            return low if self.states[low].name > name else (low + 1)
        else:
            mid = (low + high) // 2
            return self._push(low, mid, name) \
                if self.states[mid].name > name \
                else self._push(mid + 1, high, name)

    def push(self, state: State):
        self.states.insert(self._push(
            0, len(self.states) - 1, state.name), state)

    def _pick(self, low: int, high: int, name: str) -> int:
        if low > high:
            return -1
        elif low == high:
            return low if self.states[low].name == name else -1
        else:
            mid = (low + high) // 2
            return self._pick(low, mid, name) \
                if self.states[mid].name >= name \
                else self._pick(mid + 1, high, name)

    def pick(self, name: str) -> State:
        idx = self._pick(0, len(self.states) - 1, name)
        return self.states[idx] if idx != -1 else None

    def pickByStationName(self, name: str) -> List[Tuple[str, str]]:
        return reduce(lambda acc, cur: acc + cur.pickByName(name), self.states, [])

    def pickByStationId(self, _id: int) -> Station:
        obj = None
        for i in self.states:
            obj = i.pick(_id)
            if obj:
                break
        return obj

    @staticmethod
    def fromJSON(source: str) -> Places:
        try:
            with open(source, mode='r') as fd:
                placesObj = Places([])
                for i in [State.fromJSON(v, k)
                          for k, v in load(fd).items()]:
                    placesObj.push(i)
                return placesObj
        except Exception:
            return Places([])

    def toJSON(self) -> Dict[str, List[Dict[str, str]]]:
        return dict([(i.name, i.toJSON()) for i in self.states])

    @staticmethod
    def _parse(content: str) -> Places:
        '''
            Parses HTML, using BeautifulSoup.
        '''
        cityIdReg = reg_compile(r'([\d]{1,5})$')
        base_url = 'http://city.imd.gov.in/citywx/'
        placesObj = Places([])
        state_name = reg_compile(r'^(##)$')
        station_name = reg_compile(r'^(city_weather.php\?id=[\d]{1,5})$')
        root = BeautifulSoup(content, features='lxml')
        currentState = None
        for i in root.findAll('a'):
            if state_name.match(i.get('href')):
                currentState = State(i.getText(), [])
                placesObj.push(currentState)
            if station_name.match(i.get('href')):
                currentState.push(
                    Station(
                        i.getText(),
                        int(cityIdReg.search(i.get('href')).group()),
                        currentState.name,
                        urljoin(base_url, i.get('href')))
                )
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


def putAsJSON(data: Dict[str, List[Dict[str, str]]], sink: str):
    '''
        Writes collected city data i.e. corresponding state names,
        city names & urls(where weather data can be requested),
        into a JSON file
    '''
    with open(sink, mode='w') as fd:
        dump(data, fd, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
