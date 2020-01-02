#!/usr/bin/python3

from __future__ import annotations
from colorama import Fore, init as color_init
from colorama.initialise import reset_all
from os import environ
from os.path import join
import re
from sys import platform
from subprocess import run
from .places import Places
from .fetch_weather import fetch as fetchIt


def app():
    pass


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
