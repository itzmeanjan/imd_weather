#!/usr/bin/python3

from __future__ import annotations
from bs4 import BeautifulSoup, Tag
from requests import get
from urllib.parse import urljoin
from typing import Dict, Any, List, Tuple
from .forecast import Forecast, ForecastData


def _forecast(data: Tag) -> Forecast:
    '''
        Extracts next 7 day's forecast for a certain city
    '''
    return Forecast(
        list(map(lambda e:
                 ForecastData(
                     *tuple(map(lambda e:
                                urljoin('http://city.imd.gov.in/citywx/',
                                        e.find('img').get('src')) if e.findChild('img')
                                else e.getText().strip(),
                                e.findAll('td')))
                 ), data.findAll('tr')[2:])))


def _history(data: Tag) -> Dict[str, str]:
    '''
        Extracts past 24 hour's weather for a specified city
    '''
    data = data.findAll('td')[1:]
    gap = 2
    return list(map(lambda e: (e[0].getText().strip(), e[1].getText().strip()),
                    map(lambda e: data[e:e+gap], range(0, len(data), gap))))


def _parse(content: str) -> Dict[str, Any]:
    parsed = {}
    handle = BeautifulSoup(content, features='lxml')
    tables = handle.findAll('table')
    if tables[0].find('td').findChild('img'):
        parsed.update(
            {
                'location': urljoin('http://city.imd.gov.in/citywx/', tables[0].find('td').find('img').get('src'))
            })
    if tables[3].find('td').findChild('img'):
        parsed.update(
            {
                'graph': urljoin('http://city.imd.gov.in/citywx/', tables[3].find('td').find('img').get('src'))
            })
    parsed.update(
        {
            'history': _history(tables[1]),
            'forecast': _forecast(tables[2])
        })
    return parsed


def _get(url: str) -> Dict[str, Any]:
    '''
        Sends get request at imd website and returns back parsed response.
    '''
    try:
        resp = get(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/71.0'
        })
        if not resp.ok:
            raise Exception('Got {} from server'.format(resp.status_code))
        return _parse(resp.content)
    except Exception as e:
        return {'error': str(e)}


def fetch(url: str) -> Dict[str, Any]:
    return _get(url)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
