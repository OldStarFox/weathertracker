# Weather Tracker

- [Weather Tracker](#weather-tracker)
  - [Features](#features)
  - [Special Thanks and Attributions](#special-thanks-and-attributions)
  - [Getting started](#getting-started)
  - [Coming soon](#coming-soon)
  - [Getting started](#getting-started-1)
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

## Getting started

What you will need before you start:
- Open Weather API Key - Can be obtained by creating an account on their website. https://openweathermap.org/
- A Prometheus Instance
- A Grafana Instance (optional)

## Coming soon

Docker compose for the deployment of the complete stack (Weather Tracker, Prometheus and Grafana)

Pre-built Grafana Dashboard

## Getting started

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

## Docker Run
```docker
docker run -d -p "9999:9877" -e CITY="New York" -e STATE="New York" -e COUNTRY="USA" -e API_KEY="YOURAPIKEY" -e EXPORTER_PORT="9877" oldstarfox/weathertracker
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