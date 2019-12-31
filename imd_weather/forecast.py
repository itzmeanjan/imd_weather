#!/usr/bin/python3

from __future__ import annotations
from re import compile as reg_compile
from typing import List, Dict, Any


class ForecastData(object):
    '''
        Holds forecast data for a certain date
        i.e. minimum temp, maximum temp, weather condition & corresponding depiction image
    '''

    def __init__(self, date: str, _min: str, _max: str, img: str, stat: str):
        reg = reg_compile(r'^(-?\d*\.?\d{1,})$')
        self.date = date
        tmp = reg.search(_min)
        self.min = float(tmp.group()) if tmp else None
        tmp = reg.search(_max)
        self.max = float(tmp.group()) if tmp else None
        self.img = img
        self.stat = stat

    def toJSON(self) -> Dict[str, Any]:
        '''
            Helps in converting forecast of certain date into python dictionary,
            so that it can easily be written into JSON
        '''
        return {
            'date': self.date,
            'min': self.min,
            'max': self.max,
            'img': self.img,
            'status': self.stat
        }


class Forecast(object):
    '''
        Simply a list based wrapper for holding all forecast
        for all available dates for a certain place
    '''

    def __init__(self, data: List[ForecastData]):
        self.data = data

    def toJSON(self) -> List[Dict[str, Any]]:
        '''
            Converts to JSON
        '''
        return [i.toJSON() for i in self.data]


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
