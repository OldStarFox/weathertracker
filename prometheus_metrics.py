"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge
import open_weather
import logger
import logging
import atexit

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, polling_interval_seconds=5):

        log_level = os.getenv('LOG_LEVEL','INFO')
        self.log = logging.getLogger()
        if len(self.log.handlers) == 0:
            self._QueueListner, self._Queue = logger.console_logger_init(log_level)

        self.polling_interval_seconds = polling_interval_seconds
        city = os.getenv('CITY')
        if not city:
            self.log.critical('Unable to read CITY from environement')
            raise ValueError('NoneType is not a valid CITY')

        state = os.getenv('STATE')
        if not state:
            self.log.critical('Unable to read STATE from environement')
            raise ValueError('NoneType is not a valid STATE')

        country = os.getenv('COUNTRY')
        if not country:
            self.log.critical('Unable to read COUNTRY from environement')
            raise ValueError('NoneType is not a valid COUNTRY')

        self.weather = open_weather.OpenWeather(city,state,country)

        self.weather_temperature = Gauge("weather_temperature", "Open Weather Temperature in Celsius",labelnames=['city','state','country'])
        self.weather_temperature_max = Gauge("weather_temperature_max", "Open Weather Max Temperature in Celsius",labelnames=['city','state','country'])
        self.weather_temperature_min = Gauge("weather_temperature_min", "Open Weather Min Temperature in Celsius",labelnames=['city','state','country'])
        self.weather_feels_like = Gauge("weather_feels_like", "Open Weather Feels Like Temperature in Celsius",labelnames=['city','state','country'])
        self.weather_humidity = Gauge("weather_humidity", "Open Weather Humidity %",labelnames=['city','state','country'])
        self.weather_pressure = Gauge("weather_pressure", "Open Weather Pressure in hPa",labelnames=['city','state','country'])
        self.weather_visibility = Gauge("weather_visibility", "Open Weather Visibility in meters",labelnames=['city','state','country'])
        self.weather_wind_speed = Gauge("weather_wind_speed", "Open Weather Wind Speed in meters/sec",labelnames=['city','state','country'])
        self.weather_wind_degree = Gauge("weather_wind_degree", "Open Weather Wind Degree",labelnames=['city','state','country'])
        self.weather_wind_gust = Gauge("weather_wind_gust", "Open Weather Wind Gust meters/sec",labelnames=['city','state','country'])
        self.weather_rain_1h = Gauge("weather_rain_1h", "Open Weather Rain Volume 1h",labelnames=['city','state','country'])
        self.weather_snow_1h = Gauge("weather_snow_1h", "Open Weather Snow Volume 1h",labelnames=['city','state','country'])
        self.weather_clouds = Gauge("weather_clouds", "Open Weather Cloud Coverage %",labelnames=['city','state','country'])
        self.weather_uvi = Gauge("weather_uvi", "Open Weather UVI Index",labelnames=['city','state','country'])
        self.weather_dew_point = Gauge("weather_dew_point", "Open Weather Dew Point",labelnames=['city','state','country'])
        self.weather_sunrise = Gauge('weather_sunset', 'Open Weather Sunrise and Sunset',labelnames=['city','state','country'])
        self.weather_sunset = Gauge('weather_sunrise', 'Open Weather Sunrise and Sunset',labelnames=['city','state','country'])
        self.weather_aqi = Gauge("weather_aqi", "Open Weather Air Quality Index",labelnames=['city','state','country'])
        self.weather_co = Gauge("weather_co", "Open Weather Carbon monoxide (CO) in μg/m3",labelnames=['city','state','country'])
        self.weather_no = Gauge("weather_no", "Open Weather Nitrogen monoxide (NO) in μg/m3",labelnames=['city','state','country'])
        self.weather_no2 = Gauge("weather_no2", "Open Weather Nitrogen dioxide (NO2) in μg/m3",labelnames=['city','state','country'])
        self.weather_o3 = Gauge("weather_o3", "Open Weather Ozone (O3) in μg/m3",labelnames=['city','state','country'])
        self.weather_so2 = Gauge("weather_so2", "Open Weather Sulphur dioxide (SO2) in μg/m3",labelnames=['city','state','country'])
        self.weather_pm2_5 = Gauge("weather_pm2_5", "Open Weather Fine particulate matter (PM2.5) in μg/m3",labelnames=['city','state','country'])
        self.weather_pm10 = Gauge("weather_pm10", "Open Weather Fine particulate matter (PM2.5)",labelnames=['city','state','country'])
        self.weather_nh3 = Gauge("weather_nh3", "Open Weather Ammonia (NH3) in μg/m3",labelnames=['city','state','country'])

        atexit.register(self._close_log)

    def _close_log(self):
        self._QueueListner.stop()

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """
        try:
            locations = self.weather.get_weather()
            for location in locations:
                CurrentWather = location.weather
                self.weather_temperature.labels(location.city,location.state,location.country).set(CurrentWather.temperature)
                self.weather_temperature_max.labels(location.city,location.state,location.country).set(CurrentWather.temperature_max)
                self.weather_temperature_min.labels(location.city,location.state,location.country).set(CurrentWather.temperature_min)
                self.weather_feels_like.labels(location.city,location.state,location.country).set(CurrentWather.feels_like)
                self.weather_humidity.labels(location.city,location.state,location.country).set(CurrentWather.humidity)
                self.weather_pressure.labels(location.city,location.state,location.country).set(CurrentWather.pressure)
                self.weather_visibility.labels(location.city,location.state,location.country).set(CurrentWather.visibility)
                self.weather_wind_speed.labels(location.city,location.state,location.country).set(CurrentWather.wind_speed)
                self.weather_wind_degree.labels(location.city,location.state,location.country).set(CurrentWather.wind_degree)
                self.weather_wind_gust.labels(location.city,location.state,location.country).set(CurrentWather.wind_gust)
                self.weather_rain_1h.labels(location.city,location.state,location.country).set(CurrentWather.rain_1h)
                self.weather_snow_1h.labels(location.city,location.state,location.country).set(CurrentWather.snow_1h)
                self.weather_clouds.labels(location.city,location.state,location.country).set(CurrentWather.clouds)
                self.weather_uvi.labels(location.city,location.state,location.country).set(CurrentWather.uvi)
                self.weather_dew_point.labels(location.city,location.state,location.country).set(CurrentWather.dew_point)

                self.weather_sunrise.labels(location.city,location.state,location.country).set(CurrentWather.sunrise)
                self.weather_sunset.labels(location.city,location.state,location.country).set(CurrentWather.sunset)

                self.weather_aqi.labels(location.city,location.state,location.country).set(CurrentWather.aqi)
                self.weather_co.labels(location.city,location.state,location.country).set(CurrentWather.co)
                self.weather_no.labels(location.city,location.state,location.country).set(CurrentWather.no)
                self.weather_no2.labels(location.city,location.state,location.country).set(CurrentWather.no2)
                self.weather_o3.labels(location.city,location.state,location.country).set(CurrentWather.o3)
                self.weather_so2.labels(location.city,location.state,location.country).set(CurrentWather.so2)
                self.weather_pm2_5.labels(location.city,location.state,location.country).set(CurrentWather.pm2_5)
                self.weather_pm10.labels(location.city,location.state,location.country).set(CurrentWather.pm10)
                self.weather_nh3.labels(location.city,location.state,location.country).set(CurrentWather.nh3)
        except:
            self.log.exception('Unable to get Weather Information')


def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    app_metrics = AppMetrics(
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()