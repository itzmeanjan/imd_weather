#!/usr/bin/python3

from __future__ import annotations
from typing import Dict


class Station:
    def __init__(self, name: str, state: str, url: str):
        self.name = name
        self.state = state
        self.url = url

    @staticmethod
    def fromJSON(data: Dict[str, str], state: str) -> Station:
        return Station(data['name'], state, data['url'])

    def toJSON(self) -> Dict[str, str]:
        return {'name': self.name, 'url': self.url}


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
