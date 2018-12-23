#!/usr/bin/python3

'''
    Run `chmod +x install.py` before you excute this script.
    Then `./install.py` will do the installation part.
'''

try:
    from city_info import fetch
    from records import store_city_name_id
    from os import environ, getcwd, chmod
    from shutil import copytree
    from os.path import join, exists
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __is_init_setup_done__():
    home_dir = environ.get('HOME', '')
    if(not home_dir):
        print('[!]Set environment variable HOME first')
        exit(1)
    data_dir = join(home_dir, '.imd_weather')
    if(exists(data_dir)):
        return True
    return False


def __init_setup__():
    resp = fetch()
    if(resp.get('error')):
        print('[!]Couldn\'t download required data: \'{}\'\n[!]Installation \
        failed :/\n'.format(resp.get('error', '???')))
        return False
    if(store_city_name_id(resp).get('status') != 'success'):
        return False
    home_dir = environ.get('HOME')
    try:
        copytree(getcwd(), join(home_dir, '.imd_weather'))
        chmod(join(home_dir, '.imd_weather', 'imd_weather_app.py'), 0o775)  # making imd_weather_app.py executable.
        chmod(join(home_dir, '.imd_weather', 'install.py'), 0o664)  # making install.py not executable.
    except Exception as e:
        print('[!]Error : {}'.format(str(e)))
        return False
    return True


def install():
    if(__is_init_setup_done__()):
        print('[!]Installation already done')
        return
    if(__init_setup__()):
        print('[+]Successful Installation\n[+]Now add \'{}\' to your path variable and invoke \'imd_weather_app.py\' from anywhere in your directory tree.'.format(join(environ.get('HOME'), '.imd_weather')))
        return
    print('[!]Installation failed')
    return


if __name__ == '__main__':
    try:
        install()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
