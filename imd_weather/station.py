#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, Any


class Station:
    def __init__(self, name: str, _id: int, state: str, url: str):
        self.name = name
        self.id = _id
        self.state = state
        self.url = url

    @staticmethod
    def fromJSON(data: Dict[str, Any], state: str) -> Station:
        return Station(data['name'], data['id'], state, data['url'])

    def toJSON(self) -> Dict[str, Any]:
        return {'name': self.name, 'id': self.id, 'url': self.url}


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
