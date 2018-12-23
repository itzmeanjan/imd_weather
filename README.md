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
      
      Remember, I've set db_name = 'imd_city_db', if you want to use some different name for your database,
      feel free to use that for db_name parameter.

      If you pass city_name, all possible matches will be taken care of and returned. From returned dictionary, find the
      required one.

      If you pass a city_id, only full match for that city_id will be performed.
    '''
    print(fetch_city_name_id()) # will return all available records
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
  
 ## Update ::
   
  - Now you can easily install **imd_weather_app.py** and invoke it from command line for fetching Weather data from IMD.
  - I've written two new scripts and put them in this repo, which are **[install.py](https://github.com/itzmeanjan/imd_weather/blob/master/install.py)** and **[imd_weather_app.py](https://github.com/itzmeanjan/imd_weather/blob/master/imd_weather_app.py)**.
  - **install.py** will help you to install the script **imd_weather_app.py**.
  - After that **imd_weather_app.py** will become invokabale from command line.
  - I've tested installation only on Ubuntu, Fedora, Mint and Debian, where it works fine.
  - Feel free to run installation on other systems, and let me know whether it works or not.
  - I've written **install.py** for running installation procedure only for GNU/Linux based systems.
  
  ### Installation :

   Following steps will lead you to installation of **imd_weather_app.py**
  
   - First Clone this [repo](https://github.com/itzmeanjan/imd_weather/) at an appropriate location in your computer.
  
     ```
       >> git clone https://github.com/itzmeanjan/imd_weather/
     ```
  
   - Get into imd_weather directory.
  
     ```
       >> cd imd_weather
     ```
  
   - Make **install.py** executable.
  
     ```
       >> chmod +x install.py
     ```
    
   - Execute **install.py**.
  
     ```
       >> ./install.py
     ```
   
   - This will create a directory named **.imd_directory**, under **/home/your-user-name**,
   which is set as value of your **HOME** environment variable. All required files will 
   be copied to that directory.
  
  - Now you need to append **:$HOME/.imd_directory** to your **PATH** variable.
  
  - Open ~/.bash_profile using your favourite text editor.
    ```
      >> nano ~/.bash_profile
      
      or
      
      >> gedit ~/.bash_profile
    ```
  
  - Append **export PATH=$PATH:$HOME/.imd_weather** at end and save the file.
  
    ```
      export PATH=$PATH:$HOME/.imd_weather
    ```
  
  - If you find there already exists some command looking like previous one, just 
  append **:$HOME/.imd_weather** where the **export PATH=$PATH*** line ends.
  
  - Now you need to run
  
    ```
      >> source ~/.bash_profile
    ```
  
  - So **PATH** variable has got updated, which you can check by running
  
    ```
      >> echo $PATH
    ```
  
  - It's time for a reboot. Reboot your system and log into it.
  
  - Check PATH variable value from any terminal, you'll find **:$HOME/.imd_weather** appended.
  
  - Try **imd_weather_app.py** from any where in your directory tree. It'll work.
    ```
      >> imd_weather_app.py
    ```
  - As you've added **:$HOME/.imd_weather** to your PATH variable, you can now invoke **imd_weather_app.py** 
  from any where in directory tree.
  
  So, installation complete.
 
  By the way, installation isn't compulsory for using this script. You can still use it by executing 
    ```
      >> ./imd_weather_app.py
    ```
  when you're in imd_weather directory.
  
 
 As **imd_weather_app.py** uses **colorama**, a python module for coloring terminal text, you might need to install that using pip or your OS package manager. For installing it using pip, run
 
  ```
    >> pip3 install colorama --user
  ```
 
  
  Finally thanks to IMD for providing the service. More info can be found [here](http://imd.gov.in/Welcome%20To%20IMD/Welcome.php).
  Before you start using it, read below ...
  
  
  **This API is written with no intension of making any kind of misuse of IMD provided local weather forecast data. Use at your own risk. Any kind of misuse of this API is highly discouraged.**
 
 
 Hope it was helpful :)
  
