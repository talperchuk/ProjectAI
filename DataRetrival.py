import requests
import json
import pandas as pd
import numpy as np
import pathlib

apiToken = 'ApiToken f058958a-d8bd-47cc-95d7-7ecf98610e47'


def getStations(station=-1, file_name="stations_data"):
    """
    Creates all stations data (e.g. location, active status, etc.).
    Creates a json file which contains the data.
    :param station: Station id for specific station data.
    :param file_name: Beginning name for the output file.
    :return: json type element containing the data.
    """
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/',
                            headers={'Authorization': apiToken}) if station == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}'.format(station),
        headers={'Authorization': apiToken})

    with open("./data/{}.json".format(file_name), 'w') as jsonTarget:
        json.dump(response.json(), jsonTarget)
    return response.json()


def getStationDailyData(station, channel=-1, file_name=""):
    """
    Creates data for the current day for specific station.
    Creates a json file which contains the data.
    :param station: Station id for specific station data.
    :param channel: Specific channel to create data for (instead of creating for all channels).
    :param file_name: Beginning name for the output file.
    :return: json type element containing the data.
    """
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/daily'.format(station),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/daily'.format(station, channel),
        headers={'Authorization': apiToken})

    path = "./data/{}".format(station) if channel == -1 else "./data/{}/channel{}".format(station, channel)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with open("{}/{}_daily.json".format(path, file_name), 'w') as jsonTarget:
        json.dump(response.json(), jsonTarget)
    return response.json()


def getStationMonthlyData(station, channel=-1, file_name=""):
    """
    Creates data for the current month for specific station.
    Creates a json file which contains the data.
    :param station: Station id for specific station data.
    :param channel: Specific channel to create data for (instead of creating for all channels).
    :param file_name: Beginning name for the output file.
    :return: json type element containing the data.
    """
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/monthly'.format(station),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/monthly'.format(station, channel),
        headers={'Authorization': apiToken})

    path = "./data/{}".format(station) if channel == -1 else "./data/{}/channel{}".format(station, channel)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with open("{}/{}_monthly.json".format(path, file_name), 'w') as jsonTarget:
        json.dump(response.json(), jsonTarget)
    return response.json()


def getStationDailyDataForDate(station, year, month, day, channel=-1, file_name=""):
    """
    Creates data for a specific date.
    Creates a json file which contains the data.
    :param station: Station id for specific station data.
    :param year: Year of the date (e.g. 2019).
    :param month: Month of the date (e.g. 10).
    :param day: Day of the date (e.g. 25).
    :param channel: Specific channel to create data for (instead of creating for all channels).
    :param file_name: Beginning name for the output file.
    :return: json type element containing the data.
    """
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/daily/{}/{}/{}'.format(station, year, month, day),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/daily/{}/{}/{}'.format(station, channel, year, month, day),
        headers={'Authorization': apiToken})

    path = "./data/{}".format(station) if channel == -1 else "./data/{}/channel{}".format(station, channel)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with open("{}/{}_{}-{}-{}.json".format(path, file_name, year, month, day), 'w') as jsonTarget:
        json.dump(response.json(), jsonTarget)
    return response.json()


def getStationMonthlyDataForMonth(station, year, month, channel=-1, file_name=""):
    """
    Creates data for a specific month.
    Creates a json file which contains the data.
    :param station: Station id for specific station data.
    :param year: Year of the date (e.g. 2019).
    :param month: Month of the date (e.g. 10).
    :param channel: Specific channel to create data for (instead of creating for all channels).
    :param file_name: Beginning name for the output file.
    :return: json type element containing the data.
    """
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/monthly/{}/{}'.format(station, year, month),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/monthly/{}/{}'.format(station, channel, year, month),
        headers={'Authorization': apiToken})

    path = "./data/{}".format(station) if channel == -1 else "./data/{}/channel{}".format(station, channel)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with open("{}/{}_{}-{}.json".format(path, file_name, year, month), 'w') as jsonTarget:
        json.dump(response.json(), jsonTarget)
    return response.json()


def getStationRangeData(station, start_year, start_month, start_day, end_year, end_month, end_day, channel=-1, file_name=""):
    """
    Create data for range of dates.
    Creates a json file which contains the data.
    :param station: Station id for specific station data.
    :param start_year: Year of the first date.
    :param start_month: Month of the first date.
    :param start_day: Day of the first date.
    :param end_year: Year of the second date.
    :param end_month: Month of the second date.
    :param end_day: Day of the second date.
    :param channel: Specific channel to create data for (instead of creating for all channels).
    :param file_name: Beginning name for the output file.
    :return: json type element containing the data.
    """
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data?from={}/{}/{}&to={}/{}/{}'.format(station, start_year, start_month, start_day, end_year, end_month, end_day),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}?from={}/{}/{}&to={}/{}/{}'.format(station, channel, start_year, start_month, start_day, end_year, end_month, end_day),
        headers={'Authorization': apiToken})
    if 200 <= response.status_code <= 299:
        path = "./data/{}".format(station) if channel == -1 else "./data/{}/channel{}".format(station, channel)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with open("{}/{}_{}-{}-{}-{}-{}-{}.json".format(path, file_name, start_year, start_month, start_day, end_year, end_month, end_day), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
        return response.json()
    else:
        print('Response requestr failed.')
