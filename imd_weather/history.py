#!/usr/bin/python3

from __future__ import annotations
from re import compile as reg_compile
from typing import Dict, Any
from datetime import time, datetime


class History(object):
    def __init__(self, _max: str, departFromMax: str, _min: str, departFromMin: str, rainfall: str, relativeHumidityFirst: str, relativeHumidityFinal: str, sunset: str, sunrise: str, moonset: str, moonrise: str):
        self.timestamp = datetime.now().timestamp()
        reg = reg_compile(r'^(-?\d*\.?\d{1,})$')
        tmp = reg.search(_max)
        self.max = float(tmp.group()) if tmp else None
        tmp = reg.search(_min)
        self.min = float(tmp.group()) if tmp else None
        tmp = reg.search(departFromMax)
        self.departFromMax = float(tmp.group()) if tmp else None
        tmp = reg.search(departFromMin)
        self.departFromMin = float(tmp.group()) if tmp else None
        tmp = reg.search(rainfall)
        self.rainfall = float(tmp.group()) if tmp else None
        tmp = reg.search(relativeHumidityFirst)
        self.relativeHumidityAt08_30 = float(tmp.group()) if tmp else None
        tmp = reg.search(relativeHumidityFinal)
        self.relativeHumidityAt17_30 = float(tmp.group()) if tmp else None
        self.sunset = time(*[int(i, base=10) for i in sunset.split(':')])
        self.sunrise = time(*[int(i, base=10) for i in sunrise.split(':')])
        self.moonset = time(*[int(i, base=10) for i in moonset.split(':')])
        self.moonrise = time(*[int(i, base=10) for i in moonrise.split(':')])

    def toJSON(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'max': self.max,
            'departFromMax': self.departFromMax,
            'min': self.min,
            'departFromMin': self.departFromMin,
            'rainfall': self.rainfall,
            'relativeHumidityAt08:30': self.relativeHumidityAt08_30,
            'relativeHumidityAt17:30': self.relativeHumidityAt17_30,
            'sunset': self.sunset,
            'sunrise': self.sunrise,
            'moonset': self.moonset,
            'moonrise': self.moonrise
        }


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
