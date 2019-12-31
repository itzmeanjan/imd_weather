#!/usr/bin/python3

from __future__ import annotations
from re import compile as reg_compile
from typing import List, Dict, Any


class ForecastData(object):
    def __init__(self, date: str, _min: str, _max: str, img: str, stat: str):
        reg = reg_compile(r'^(\d*\.\d{1,})$')
        self.date = date
        tmp = reg.search(_min)
        self.min = float(tmp.group()) if tmp else None
        tmp = reg.search(_max)
        self.max = float(tmp.group()) if tmp else None
        self.img = img
        self.stat = stat

    def toJSON(self) -> Dict[str, Any]:
        return {
            'date': self.date,
            'min': self.min,
            'max': self.max,
            'img': self.img,
            'status': self.stat
        }


class Forecast(object):
    def __init__(self, data: List[ForecastData]):
        self.data = data

    def toJSON(self) -> List[Dict[str, Any]]:
        return [i.toJSON() for i in self.data]


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
