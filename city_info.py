#!/usr/bin/python3

try:
    from requests import get
    import re
    from bs4 import BeautifulSoup
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __parse_content__(content):
    '''
        Parsing of html page is done here, using BeautifulSoup.
    '''
    parsed = {}
    try:
        handle = BeautifulSoup(content, features='lxml')
        regex_1 = re.compile(r'^(##)$')
        regex_2 = re.compile(r'^(city_weather.php\?id=[\d]{1,5})$')
        target = handle.find('a')
        key = ''
        tmp = []
        while(target):
            if(regex_1.match(target.get('href'))):
                key = target.getText()
                tmp = []
                parsed.update({key: []})
            if(regex_2.match(target.get('href'))):
                tmp.append({target.getText(): target.get('href')})
                parsed.update({key: tmp})
            target = target.findNext('a')
    except Exception as e:
        parsed = {'error': str(e)}
    return parsed


def __get_content__(base_url):
    '''
        Performs get request at provided url and parses response.
    '''
    try:
        resp = get(base_url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/62.0'})
        if(not resp.ok):
            raise Exception('got {} from server'.format(resp.status_code))
        return __parse_content__(resp.content)
    except Exception as e:
        return {'error': str(e)}


def fetch(base_url='http://city.imd.gov.in/citywx/menu.php'):
    '''
        Simply fetches city names, corresponding url and city id from IMD website,
        parses them and returns a python dict.
    '''
    return __get_content__(base_url)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
