import requests
import json
import pandas as pd
from getChannels import getChannelIds
from getChannels import tests
from pandas.io.json import json_normalize

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
        with open(file_name, 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getAllChannelsDataFromDailyJSON(file_name = 'dailyTarget.json'):
    with open("dailyTarget.json", 'r') as f:
        data = json.load(f)
    station_id =  data['stationId']
    data_as_str = json.dumps(data['data'])
    data_pd = pd.read_json(data_as_str, orient='records', typ='series')
    measurment_times = []
    measurment_channels = {}
    for measurment in data_pd:
        measurment_times.append(measurment['datetime'])
        channels = measurment['channels']
        for channel in channels:
            if channel['name'] in measurment_channels:
                measurment_channels[channel['name']].append(channel['value'])
            else:
                measurment_channels[channel['name']] = [channel['value']]
    return station_id, measurment_times, measurment_channels





if __name__ == '__main__':
    getAllChannelsDataFromDailyJSON()
    tests()
