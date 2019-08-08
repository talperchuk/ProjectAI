import requests
import json
import pandas as pd
from getChannels import getChannelIds
from getChannels import tests
from pandas.io.json import json_normalize
from DataProcess import *

apiToken = 'ApiToken f058958a-d8bd-47cc-95d7-7ecf98610e47'


def getStationDailyData(station, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/daily'.format(station),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/daily'.format(station, channel),
        headers={'Authorization': apiToken})

    # response = requests.get('https://api.ims.gov.il/v1/envista/stations', headers={'Authorization': apiToken})
    # response = requests.get('https://api.ims.gov.il/v1/envista/stations/43/data/daily', headers={'Authorization': apiToken})
    #print(response.content)

    if file_name != "":
        with open("./data/{}_daily.json".format(file_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationMonthlyData(station, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/monthly'.format(station),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/monthly'.format(station, channel),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_monthly.json".format(file_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationDailyDataForDate(station, year, month, day, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/daily/{}/{}/{}'.format(station, year, month, day),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/daily/{}/{}/{}'.format(station, channel, year, month, day),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_{}-{}-{}.json".format(file_name, year, month, day), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationMonthlyDataForMonth(station, year, month, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/monthly/{}/{}'.format(station, year, month),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/monthly/{}/{}'.format(station, channel, year, month),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_{}-{}.json".format(file_name, year, month), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationRangeData(station, start_year, start_month, start_day, end_year, end_month, end_name, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data?from={}/{}/{}&to={}/{}/{}'.format(station, start_year, start_month, start_day, end_year, end_month, end_name),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}?from={}/{}/{}&to={}/{}/{}'.format(station, channel, start_year, start_month, start_day, end_year, end_month, end_name),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_{}-{}-{}-{}-{}-{}.json".format(file_name, start_year, start_month, start_day, end_year, end_month, end_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getChannelsDataFromJSON(file_name='dailyTarget.json'):
    with open('./data/' + file_name, 'r') as f:
        data = json.load(f)
    station_id = data['stationId']
    data_as_str = json.dumps(data['data'])
    data_pd = pd.read_json(data_as_str, orient='records', typ='series')
    #print(data_pd)
    measurments_summary = {}
    measurment_times = []
    for measurment in data_pd:
        measurment_channels = {}
        measurment_times.append(measurment['datetime'])
        measurment_channels['datetime'] = (measurment['datetime'])
        channels = measurment['channels']
        for channel in channels:
            if channel['name'] in measurment_channels:
                measurment_channels[channel['name']].append(channel['value'])
            else:
                measurment_channels[channel['name']] = [channel['value']]
        measurments_summary[measurment['datetime']] = measurment_channels
    return station_id, measurment_times, measurment_channels, measurments_summary


if __name__ == '__main__':
    #getStationDailyData(43, channel=8, file_name="ch8")
    #getStationMonthlyData(43, file_name="aug")
    #getStationDailyDataForDate(43, year=2019, month=8, day=1, file_name="day")
    #getStationMonthlyDataForMonth(43, year=2019, month=7, file_name="july")
    #getStationRangeData()
    features = getChannelIds()
    print(features.keys())
    print(list(features))
    print(features.values())
    id, times, channels, msrmnts = getChannelsDataFromJSON(file_name='july_2019-7.json')
    print(features)
    print("*******id******")
    print(id)
    print("*******times******")
    print(times)
    print("*******channels******")
    print(channels)
    print("*******dataFrames****")
    datafs = createDataFrame(file_name='july_2019-7.json')
    print(datafs)
    #tests()
