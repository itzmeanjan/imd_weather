#!/usr/bin/python3

try:
    from urllib.parse import urlencode
    from bs4 import BeautifulSoup
    from requests import get
    from records import __validate_city_id__, fetch_city_name_id
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __extract_7_days_forecast__(data):
    '''
        next 7 days forecast data gets extracted from web page by this function.
    '''
    parsed = []
    try:
        data = data.findAll('tr')[2:]
        for i in data:
            tmp = []
            for j in i.findAll('td'):
                if(j.findChild('img')):
                    tmp.append(j.find('img').get('src'))
                else:
                    tmp.append(j.getText().strip())
            parsed.append(tmp)
    except Exception as e:
        parsed = [str(e)]
    return parsed


def __extract_past_24_hours_weather_data__(data):
    '''
        past 24 hours weather data extracted from web page, here.
    '''
    parsed = {}
    try:
        data = data.findAll('td')[1:]
        gap = 2
        conflict = 'Departure from Normal(oC)'
        conflict_count = 0
        for i in range(0, len(data), gap):
            tmp = data[i:i+gap]
            if(tmp[0].getText().strip() == conflict):
                parsed.update({tmp[0].getText().strip()+'{}'.format(conflict_count): tmp[1].getText().strip()})
                conflict_count += 1
            else:
                parsed.update({tmp[0].getText().strip(): tmp[1].getText().strip()})
    except Exception as e:
        parsed = {'error': str(e)}
    return parsed


def __parse_content__(content):
    '''
        Parse content using BeautifulSoup, returns python dict.
    '''
    parsed = {}
    try:
        handle = BeautifulSoup(content, features='lxml')
        tables = handle.findAll('table')
        if(tables[0].find('td').findChild('img')):
            parsed.update({'location_image': tables[0].find('td').find('img').get('src')})
        parsed.update({'past_24_hours_weather': __extract_past_24_hours_weather_data__(tables[1])})
        parsed.update({'7_days_forecast': __extract_7_days_forecast__(tables[2])})
        if(tables[3].find('td').findChild('img')):
            parsed.update({'summary_image': tables[3].find('td').find('img').get('src')})
    except Exception as e:
        parsed = {'error': str(e)}
    return parsed


def __get_content__(base_url):
    '''
        Sends get request at imd website and returns back parsed response.
    '''
    try:
        resp = get(base_url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/62.0'})
        if(not resp.ok):
            raise Exception('got {} from server'.format(resp.status_code))
        return __parse_content__(resp.content)
    except Exception as e:
        return {'error': str(e)}


def fetch(city_id, override_check=False, db_name='imd_weather_record', base_url='http://city.imd.gov.in/citywx/city_weather.php'):
    '''
        Fetches weather info of certain city, designated by city_id, from imd website and returns in parsed form.
        set `override_check` to True, if you have'nt yet stored city name & id, into local database.
        city_id is mandatory argument.
    '''
    if(__validate_city_id__(city_id)):
        if(override_check):
            return {city_id: __get_content__(base_url+'?{}'.format(urlencode([('id', city_id)])))}
        if(fetch_city_name_id(city_id=city_id, db_name=db_name).get(city_id, [])):
            return {city_id: __get_content__(base_url+'?{}'.format(urlencode([('id', city_id)])))}
    return {'error': 'city id not validated'}


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)