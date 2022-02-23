from sre_parse import State
import requests
import time
from dataclasses import dataclass
import logger
import os
import atexit
import logging
from ast import literal_eval

@dataclass
class Weather():
    temperature: float = 0
    temperature_max: float = 0
    temperature_min: float = 0
    feels_like: float = 0
    humidity: float = 0
    pressure: float = 0
    visibility: float = 0
    wind_speed: float = 0
    wind_degree: float = 0
    wind_gust: float = 0
    sunrise: int = 0
    sunset: int = 0
    snow_1h: float = 0
    rain_1h: float = 0
    clouds: int = 0
    uvi: float = 0
    dew_point: float = 0
    aqi: int = 0
    co: float = 0
    no: float = 0
    no2: float = 0
    o3: float = 0
    so2: float = 0
    pm2_5: float = 0
    pm10: float = 0
    nh3: float = 0

@dataclass
class Location():
    city : str
    state : str
    country : str
    weather : Weather
    lat : float = 0
    long : float = 0
class OpenWeather():

    def __init__(self,city,state,country) -> None:

        log_level = os.getenv('LOG_LEVEL','INFO')
        self.log = logging.getLogger()
        if len(self.log.handlers) == 0:
            self._log_close=True
            self._QueueListner, self._Queue = logger.console_logger_init(log_level)

        self._BASE_URL = "https://api.openweathermap.org/"
        self._SECONDS_IN_DAY = 86400
        self._last_one_api_call = None
        self._last_weather_api_call = None
        self._last_air_polution_api_call = None
        self._last_one_api_call_rate_warning = False
        self._last_weather_api_call_rate_warning = False
        self._last_air_polution_api_call_rate_warning = False

        try:
            self._CITY = literal_eval(str(city))
        except:
            self._CITY = city
        
        try:
            self._STATE = literal_eval(str(state))
        except:
            self._STATE = state

        try:
            self._COUNTRY = literal_eval(str(country))
        except:
            self._COUNTRY = country

        self.log.info(f'Selected city: {self._CITY}')
        self.log.info(f'Selected sates: {self._STATE }')
        self.log.info(f'Selected country: {self._COUNTRY}')
        
        assert isinstance(self._CITY,(list,str)) and isinstance(self._STATE,(list,str)) and isinstance(self._COUNTRY,(list,str)),'Wrong type of parameters passed for CITY,STATE and COUNTRY'

        self._locations=[]
        if isinstance(self._CITY,list):
            assert len(self._CITY) == len(self._STATE) == len(self._COUNTRY), 'CITY, STATE and COUNTRY lists must be of same size'
            for i in range(0,len(self._CITY)):
                self._locations.append(Location(self._CITY[i],self._STATE[i],self._COUNTRY[i],weather=Weather()))
        else:
            self._locations.append(Location(self._CITY,self._STATE,self._COUNTRY,weather=Weather()))

        self.start = None
        self.end = None

        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            self.log.critical('Unable to read API KEY from environement')
            raise ValueError('NoneType is not a valid API KEY')

        self._ONE_API_RATE = self._get_rate('ONE_API_DAILY_RATE_LIMIT',1000)
        self._WEATHER_API_RATE = self._get_rate('WEATHER_API_DAILY_RATE_LIMIT',86400)
        self._AIR_POLUTION_API_RATE = self._get_rate('AIR_POLUTION_API_DAILY_RATE_LIMIT',86400)

        atexit.register(self._close_log)

        self._get_geo_api()

    def _close_log(self):
        if self._log_close:
            self._QueueListner.stop()

    def _get_rate(self,var_name,default):
        rate = os.getenv(var_name)
        if not rate:
            rate = default
            self.log.warning(f'Environment Variable {var_name} not found, using default of {rate}')
        return int(rate)

    def _get_weather_api(self,lat,long,weather) -> None:
        url = f'{self._BASE_URL}/data/2.5/weather?lat={lat}&lon={long}&appid={self.api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            main = data['main']
            # getting temperature
            weather.temperature = main['temp'] - 273.15
            weather.temperature_max = main['temp_max'] - 273.15
            weather.temperature_min = main['temp_min'] - 273.15
            weather.feels_like = main['feels_like'] - 273.15
            # getting the humidity
            weather.humidity = main['humidity']
            # getting the pressure
            weather.pressure = main['pressure']
            weather.visibility = data['visibility']
            weather.wind_speed = data['wind'].get('speed') 
            weather.wind_degree = data['wind'].get('deg') 
            weather.wind_gust = data['wind'].get('gust')
            weather.sunrise = data['sys'].get('sunrise')
            weather.sunset = data['sys'].get('sunset')
            weather.clouds = data['clouds'].get('all')
            rain = data.get('rain')
            weather.rain_1h = rain.get('1h') if rain else 0
            snow = data.get('snow')
            weather.snow_1h = snow.get('1h') if snow else 0
        except:
            self.log.exception('Failed to request data from the weather api')
            return weather

        return weather

    def _get_geo_api(self):

        for i in self._locations:
            url = f"{self._BASE_URL}/geo/1.0/direct?q={i.city},{i.state},{i.country}&appid={self.api_key}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                coord = response.json()[0]
                city = coord.get('name') 
                country = coord.get('country') 
                state = coord.get('state') 
                i.lat = coord.get('lat')
                i.long = coord.get('lon')
                self.log.info(f'Location Identified: {city}, {state}, {country} - Coordinates: {i.lat},{i.long}')
            except:
                self.log.fatal('Unable to get geo location')
                raise

        return None

    def _get_air_polution_api(self,lat,long,weather) -> Weather:
        url = f'{self._BASE_URL}/data/2.5/air_pollution?lat={lat}&lon={long}&appid={self.api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            res = response.json()
            main = res.get('list')[0]
            components = main.get('components')
            weather.aqi = main.get('main')['aqi']
            weather.co = components.get('co')
            weather.no = components.get('no')
            weather.no2 = components.get('no2')
            weather.o3 = components.get('o3')
            weather.so2 = components.get('so2')
            weather.pm2_5 = components.get('pm2_5')
            weather.pm10 = components.get('pm10')
            weather.nh3 = components.get('nh3')
        except:
            self.log.exception('Failed to request data from the air polution api')
            return weather

        return weather

    def _get_one_api(self,lat,long,weather) -> Weather:
        url = f'{self._BASE_URL}/data/2.5/onecall?lat={lat}&lon={long}&exclude=minutely,hourly,daily&appid={self.api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            main = response.json()['current']
            weather.uvi = main['uvi']
            weather.dew_point = main['dew_point'] - 273.15
        except:
            self.log.exception('Failed to request data from the one api')
            return weather

        return weather

    def calculate_rate(self,last_call_time,rate) -> bool:
        last_call_time = 0 if not last_call_time else last_call_time
        if time.time() - last_call_time > (self._SECONDS_IN_DAY/rate)/len(self._locations):
            return True
        else:
            return False

    def get_weather(self) -> list:
        weather_call = False
        one_call = False
        air_call = False
        for location in self._locations:
            if self.calculate_rate(self._last_weather_api_call,self._WEATHER_API_RATE):
                location.weather = self._get_weather_api(location.lat,location.long,location.weather)
                weather_call = True
            else:
                if not self._last_weather_api_call_rate_warning : self.log.warning('Weather API rate limited')
                self._last_weather_api_call_rate_warning = True

            if self.calculate_rate(self._last_one_api_call,self._ONE_API_RATE):
                location.weather = self._get_one_api(location.lat,location.long,location.weather)
                one_call = True
            else:
                if not self._last_one_api_call_rate_warning : self.log.warning('One API rate limited')
                self._last_one_api_call_rate_warning = True


            if self.calculate_rate(self._last_air_polution_api_call,self._AIR_POLUTION_API_RATE):
                location.weather = self._get_air_polution_api(location.lat,location.long,location.weather)
                air_call = True
            else:
                if not self._last_air_polution_api_call_rate_warning : self.log.warning('Air Polution API rate limited')
                self._last_air_polution_api_call_rate_warning = True
            
        if weather_call: self._last_weather_api_call = time.time()
        if one_call: self._last_one_api_call = time.time()
        if air_call: self._last_air_polution_api_call = time.time()

        return self._locations