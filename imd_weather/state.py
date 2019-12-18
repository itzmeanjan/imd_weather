#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict
from .station import Station


class State:
    def __init__(self, name: str, stations: List[Station]):
        self.name = name
        self.stations = stations

    @staticmethod
    def fromJSON(data: List[Dict[str, str]], state: str) -> State:
        return State(state, [Station.fromJSON(i, state) for i in data])

    def toJSON(self) -> List[Dict[str, str]]:
        return [i.toJSON() for i in self.stations]


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
