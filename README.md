# imd_weather
A simple python API, helps you to fetch City Weather data from Indian Meteorological Dept.


## Important Points ::

  - This API uses [IMD](http://city.imd.gov.in/citywx/localwx.php), as its datasource.
  - Returns local weather forecast in processed python dictionary format.
  - It uses plyvel, a python wrapper for accessing levelDB, for storing records.
  - First it fetches all city names & ids along with their weather data links and stores them.
  - Then using a certain **city_id**, fetches **7 days weather forecast** & **last 24 hours weather data** from IMD, which can be stored in local database.
 
 
### Example Usage of API :


  #### imd_weather.city_info :
  
  ```
    from imd_weather.city_info import fetch
    '''
      Simply fetches city names, corresponding url and city id from IMD website,
      parses them and returns a python dict.
    '''
    print(fetch())
  ```
  
  #### imd_weather.records :
  
  ```
    from imd_weather.records import fetch_city_name_id, store_city_name_id
    '''
      If you want to store, just fetched city names, ids and weather data links in local levelDB, use this function.
      returns a dict, specifing status of task.
    '''
    print(store_city_name_id(data)) # data = imd_weather.city_info.fetch()
    '''
      Fetches stored data from local database.
    '''
    print(fetch_city_name_id()) # will return all available records
    # remember, I've set db_name = 'imd_weather_record', if you want to use some different name for your database,
    # feel free to use that for db_name parameter.
    # if you pass city_name, all possible matches will be taken care of and returned. From returned dictionary, find the
    # required one.
  ```
  
  #### imd_weather.weather :
  
  ```
    from imd_weather.weather import fetch as fetch_weather
    '''
      There's one override_check parameter, which is set to False, set it to True, if you want provided city_id not to be
      cross-checked with existing database. db_name is also set to its default value 'imd_weather_record'.
    '''
    print(fetch_weather('xxxxx')) # city_id, mandatory argument.
  ```
  
  
  Now thanks to IMD for providing the service. More info can be found [here](http://imd.gov.in/Welcome%20To%20IMD/Welcome.php).
  Before you start using it, read below ...
  
  
  **This API is written with no intension of making any kind of misuse of IMD provided local weather forecast data. Use at your own risk. Any kind of misuse of this API is highly discouraged.**
 
 
 Hope it was helpful :)
  
