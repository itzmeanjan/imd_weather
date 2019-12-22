#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict
from .station import Station


class State:
    def __init__(self, name: str, stations: List[Station]):
        self.name = name
        self.stations = stations

    def _push(self, low: int, high: int, _id: int) -> int:
        if low > high:
            return 0
        elif low == high:
            return low if self.stations[low].id > _id else (low + 1)
        else:
            mid = (low + high) // 2
            return self._push(low, mid, _id) \
                if self.stations[mid].id > _id \
                else self._push(mid + 1, high, _id)

    def push(self, station: Station):
        self.stations.insert(self._push(
            0, len(self.stations) - 1, station.id), station)

    def _pick(self, low: int, high: int, _id: int) -> int:
        if low > high:
            return -1
        elif low == high:
            return low if self.stations[low].id == _id else -1
        else:
            mid = (low + high) // 2
            return self._pick(low, mid, _id) \
                if self.stations[mid].id >= _id \
                else self._pick(mid + 1, high, _id)

    def pick(self, _id: int) -> Station:
        idx = self._pick(0, len(self.stations) - 1, _id)
        return self.stations[idx] if idx != -1 else None

    def pickByName(self, name: str) -> Station:
        obj = None
        for i in self.stations:
            if i.name == name:
                obj = i
                break
        return obj

    @staticmethod
    def fromJSON(data: List[Dict[str, str]], state: str) -> State:
        stateObj = State(state, [])
        for i in [Station.fromJSON(i, state)
                  for i in data]:
            stateObj.push(i)
        return stateObj

    def toJSON(self) -> List[Dict[str, str]]:
        return [i.toJSON() for i in self.stations]


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
