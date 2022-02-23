# Weather Tracker

- [Weather Tracker](#weather-tracker)
  - [Features](#features)
  - [Special Thanks and Attributions](#special-thanks-and-attributions)
  - [Before You Start](#before-you-start)
  - [Coming soon](#coming-soon)
  - [Getting Started](#getting-started)
  - [Sample Output](#sample-output)
  - [Docker Run](#docker-run)
  - [Docker Compose](#docker-compose)
  - [Docker Hub Page](#docker-hub-page)
  - [Git Hub Page](#git-hub-page)
  - [Limitations](#limitations)

## Features

- Live Weather Data from Open Weather
- Support for Multiple Locations
- API Call Rate automatically adjusts to number of tracked cities
- Exposes Metrics to Prometheus via Prometheus Client

## Special Thanks and Attributions

Open Weather Map: This project was only possible because of the nice people at Open Weather making their APIs freely available to the public. https://openweathermap.org/

Thomas Stringer: I used Thomas Stringer post to kick start the Prometheus metrics export. I did alterations to expose the weather metrics but the code is basically the same: https://trstringer.com/quick-and-easy-prometheus-exporter/

## Before You Start

What you will need before you start:
- Open Weather API Key - Can be obtained by creating an account on their website. https://openweathermap.org/
- A Prometheus Instance
- A Grafana Instance (optional)

## Coming soon

Docker compose for the deployment of the complete stack (Weather Tracker, Prometheus and Grafana)

Pre-built Grafana Dashboard

## Getting Started

Weather Tracker exposes live weather data to be consumed by Prometheus allowing metrics tracking and plotting via Grafana (or other tool of choice). Currently the following weather data is available:
- Temperature in Celsius
- Max Temperature in Celsius
- Min Temperature in Celsius
- Feels Like Temperature in Celsius
- Humidity
- Pressure in hPa
- Visibility in meters
- Wind Speed in meters/sec
- Wind Degree
- Wind Gust meters/sec
- Rain Volume 1h
- Snow Volume 1h
- Cloud Coverage %
- UVI Index
- Dew Point
- Sunrise and Sunset
- Sunrise and Sunset
- Air Quality Index
- Carbon monoxide (CO) in μg/m3
- Nitrogen monoxide (NO) in μg/m3
- Nitrogen dioxide (NO2) in μg/m3
- Ozone (O3) in μg/m3
- Sulphur dioxide (SO2) in μg/m3
- Fine particulate matter (PM2.5) in μg/m3
- Fine particulate matter (PM2.5)
- Ammonia (NH3) in μg/m3

With the applicaiton up and running you can create a new target on Prometheus to collect the metrics.
Visiting your host ip address or domain on the defined port will yield the following [output](#sample-output)

## Sample Output

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 150.0
python_gc_objects_collected_total{generation="1"} 228.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 58.0
python_gc_collections_total{generation="1"} 5.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="8",patchlevel="12",version="3.8.12"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.33553664e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.8028928e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.64562656969e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.19
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 10.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP weather_temperature Open Weather Temperature in Celsius
# TYPE weather_temperature gauge
weather_temperature{city="New York",country="USA",state="New York"} 14.850000000000023
# HELP weather_temperature_max Open Weather Max Temperature in Celsius
# TYPE weather_temperature_max gauge
weather_temperature_max{city="New York",country="USA",state="New York"} 17.400000000000034
# HELP weather_temperature_min Open Weather Min Temperature in Celsius
# TYPE weather_temperature_min gauge
weather_temperature_min{city="New York",country="USA",state="New York"} 10.629999999999995
# HELP weather_feels_like Open Weather Feels Like Temperature in Celsius
# TYPE weather_feels_like gauge
weather_feels_like{city="New York",country="USA",state="New York"} 14.510000000000048
# HELP weather_humidity Open Weather Humidity %
# TYPE weather_humidity gauge
weather_humidity{city="New York",country="USA",state="New York"} 81.0
# HELP weather_pressure Open Weather Pressure in hPa
# TYPE weather_pressure gauge
weather_pressure{city="New York",country="USA",state="New York"} 1014.0
# HELP weather_visibility Open Weather Visibility in meters
# TYPE weather_visibility gauge
weather_visibility{city="New York",country="USA",state="New York"} 10000.0
# HELP weather_wind_speed Open Weather Wind Speed in meters/sec
# TYPE weather_wind_speed gauge
weather_wind_speed{city="New York",country="USA",state="New York"} 5.36
# HELP weather_wind_degree Open Weather Wind Degree
# TYPE weather_wind_degree gauge
weather_wind_degree{city="New York",country="USA",state="New York"} 360.0
# HELP weather_wind_gust Open Weather Wind Gust meters/sec
# TYPE weather_wind_gust gauge
weather_wind_gust{city="New York",country="USA",state="New York"} 8.49
# HELP weather_rain_1h Open Weather Rain Volume 1h
# TYPE weather_rain_1h gauge
weather_rain_1h{city="New York",country="USA",state="New York"} 0.0
# HELP weather_snow_1h Open Weather Snow Volume 1h
# TYPE weather_snow_1h gauge
weather_snow_1h{city="New York",country="USA",state="New York"} 0.0
# HELP weather_clouds Open Weather Cloud Coverage %
# TYPE weather_clouds gauge
weather_clouds{city="New York",country="USA",state="New York"} 75.0
# HELP weather_uvi Open Weather UVI Index
# TYPE weather_uvi gauge
weather_uvi{city="New York",country="USA",state="New York"} 0.76
# HELP weather_dew_point Open Weather Dew Point
# TYPE weather_dew_point gauge
weather_dew_point{city="New York",country="USA",state="New York"} 11.480000000000018
# HELP weather_sunset Open Weather Sunrise and Sunset
# TYPE weather_sunset gauge
weather_sunset{city="New York",country="USA",state="New York"} 1.645616349e+09
# HELP weather_sunrise Open Weather Sunrise and Sunset
# TYPE weather_sunrise gauge
weather_sunrise{city="New York",country="USA",state="New York"} 1.645655997e+09
# HELP weather_aqi Open Weather Air Quality Index
# TYPE weather_aqi gauge
weather_aqi{city="New York",country="USA",state="New York"} 1.0
# HELP weather_co Open Weather Carbon monoxide (CO) in μg/m3
# TYPE weather_co gauge
weather_co{city="New York",country="USA",state="New York"} 333.79
# HELP weather_no Open Weather Nitrogen monoxide (NO) in μg/m3
# TYPE weather_no gauge
weather_no{city="New York",country="USA",state="New York"} 1.57
# HELP weather_no2 Open Weather Nitrogen dioxide (NO2) in μg/m3
# TYPE weather_no2 gauge
weather_no2{city="New York",country="USA",state="New York"} 25.02
# HELP weather_o3 Open Weather Ozone (O3) in μg/m3
# TYPE weather_o3 gauge
weather_o3{city="New York",country="USA",state="New York"} 26.82
# HELP weather_so2 Open Weather Sulphur dioxide (SO2) in μg/m3
# TYPE weather_so2 gauge
weather_so2{city="New York",country="USA",state="New York"} 3.99
# HELP weather_pm2_5 Open Weather Fine particulate matter (PM2.5) in μg/m3
# TYPE weather_pm2_5 gauge
weather_pm2_5{city="New York",country="USA",state="New York"} 5.79
# HELP weather_pm10 Open Weather Fine particulate matter (PM2.5)
# TYPE weather_pm10 gauge
weather_pm10{city="New York",country="USA",state="New York"} 9.26
# HELP weather_nh3 Open Weather Ammonia (NH3) in μg/m3
# TYPE weather_nh3 gauge
weather_nh3{city="New York",country="USA",state="New York"} 0.9
```

## Docker Run
```docker
docker run -d -p "9877:9877" -e CITY="New York" -e STATE="New York" -e COUNTRY="USA" -e API_KEY="YOURAPIKEY" -e EXPORTER_PORT="9877" oldstarfox/weathertracker
```

## Docker Compose

```yaml
version: "3.3"

services:
  weathertracker:
    image: oldstarfox/weathertracker:latest
    restart: unless-stopped
    ports:
      - "9877:9877"
    environment:
    - EXPORTER_PORT=9877 #Needs to match container ports
    - CITY=**CITY_NAME** #Can be a single city i.e: "New York" or an array i.e: ["New York","San Francisco"]
    - STATE=**STATE_NAME** #Can be a single city i.e: "New York" or an array i.e: ["New York","California"]
    - COUNTRY=**COUNTRY CODE** #Can be a single city i.e: "USA" or an array i.e: ["USA","USA"]
    - POLLING_INTERVAL_SECONDS=15 #How frequently the weather data will be sourced.
    - API_KEY=**OPEN WHEATER API KEY** # YOUR Open weather API Key
    - ONE_API_DAILY_RATE_LIMIT=1000
    - WEATHER_API_DAILY_RATE_LIMIT=86400
    - AIR_POLUTION_API_DAILY_RATE_LIMIT=86400
```

## Docker Hub Page
[Docker Hub](https://hub.docker.com/r/oldstarfox/weathertracker)

## Git Hub Page
[Git Hub](https://github.com/OldStarFox/weathertracker)

## Limitations

Open Weather Map data is limited by the number of API calls in a 24 hour period and they have different rates. The application was built with this in mind and will rate limit the calls to not go over the thresholds. If you are using a payed service from Open Weather you may override the rates using the following environment variables on your docker container.
- ONE_API_DAILY_RATE_LIMIT=1000 (default)
- WEATHER_API_DAILY_RATE_LIMIT=86400 (default)
- AIR_POLUTION_API_DAILY_RATE_LIMIT=86400 (default)