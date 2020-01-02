#!/usr/bin/python3

from __future__ import annotations
from .history import History
from .forecast import Forecast
from typing import Dict, Any


class WeatherAtStation(object):
    def __init__(self, stationName: str, stationId: int, history: History, forecast: Forecast, loc: str, graph: str):
        self.name = stationName
        self.id = stationId
        self.history = history
        self.forecast = forecast
        self.location = loc
        self.graph = graph

    def toJSON(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'id': self.id,
            'history': self.history.toJSON(),
            'forecast': self.forecast.toJSON(),
            'location': self.location,
            'graph': self.graph
        }

    @staticmethod
    def fromJSON(data: Dict[str, Any]) -> WeatherAtStation:
        return WeatherAtStation(data.get('name'), data.get('id'),
                                History.fromJSON(data.get('history')), Forecast.fromJSON(
                                    data.get('forecast')),
                                data.get('location'), data.get('graph'))


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
