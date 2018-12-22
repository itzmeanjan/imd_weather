#!/usr/bin/python3

try:
    from plyvel import DB, Error as plError
    import re
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __match_city_name__(city_name, itr):
    '''
        itr is levelDB iterator object, which iterates over levelDB key-value pairs,
        and return matched result(s) back, if any.
    '''
    resp = {}
    regex = re.compile(r'.*({}).*'.format(city_name), flags=re.I)
    try:
        for i, j in itr:
            tmp = j.decode('utf-8').split(';')
            if(regex.match(tmp[1])):
                resp.update({i.decode('utf-8'): tmp})
        itr.close()
    except plError as e:
        resp = {'status': str(e)}
    except Exception as e:
        resp = {'status': str(e)}
    return resp


def __validate_city_id__(city_id):
    reg = re.compile(r'^(\d{1,5})$')
    if(reg.match(city_id)):
        return True
    return False


def __format_db_entry__(data):
    '''
        Formats City Name-ID-Link entry properly, so that it's okay to put them into database.
    '''
    formatted = {}
    try:
        regex = re.compile(r'^(city_weather.php\?id=([\d]{1,5}))$')
        for i, j in data.items():
            for k in j:
                for l, m in k.items():
                    match_obj = regex.match(m)
                    if(match_obj):
                        formatted.update({match_obj.groups()[1].encode('utf-8'): '{};{};{}'.format(i, l, m).encode('utf-8')})
    except Exception as e:
        formatted = {'error': str(e)}
    return formatted


def store_city_name_id(data, db_name='imd_weather_record'):
    '''
        Stores City Names, IDs and correspoding links into a local levelDB.
        City ID is used as key value.
    '''
    resp = {}
    try:
        db_handle = DB(db_name, create_if_missing=True)
        data = __format_db_entry__(data)
        for i, j in data.items():
            db_handle.put(i, j)
        db_handle.close()
        resp = {'status': 'success'}
    except plError as e:
        resp = {'status': str(e)}
    except Exception as e:
        resp = {'status': str(e)}
    return resp


def fetch_city_name_id(city_id='', city_name='', db_name='imd_weather_record'):
    '''
        City Names, IDs and corresponding links are fetched from local levelDB.
        If you pass city_id and city_name both, city_id would be chosen over city_name,
        for lookup.
        Passing only city_name, would help you to find possible matches.
        If you pass no arguments, then all available records will be returned back.
    '''
    resp = {}
    try:
        db_handle = DB(db_name, create_if_missing=True)
        if(city_id):
            if(not __validate_city_id__(city_id)):
                raise Exception('city id not validated')
            tmp = db_handle.get(city_id.encode('utf-8'), b'')
            if(tmp):
                resp.update({city_id: tmp.decode('utf-8').split(';')})
            else:
                resp = {'status': 'record not found'}
        elif(city_name):
            resp.update(__match_city_name__(city_name, db_handle.iterator()))
        else:
            itr = db_handle.iterator()
            for i, j in itr:
                resp.update({i.decode('utf-8'): j.decode('utf-8').split(';')})
            itr.close()
        db_handle.close()
    except plError as e:
        resp = {'status': str(e)}
    except Exception as e:
        resp = {'status': str(e)}
    return resp


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
