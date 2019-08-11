
from DataRetrival import *
from GetChannels import getChannelIds
from pandas.io.json import json_normalize


def tests():
    # getDailyData(file_name='dailyTarget.json')
    channels = getChannelIds()

    with open("dailyTarget.json", 'r') as f:
        data = json.load(f)
        print(data)
        print('****')
        d = json.dumps(data['data'])
        print("****t****")
        t = pd.read_json(d, orient='records', typ='series')
        print(t[0]['channels'][0])
        data_norm = json_normalize(data=data['data'])
        print("****tt****")

        print(data_norm.to_json())

        print("****tend****")

        c = data['data'][0]['channels'][0]['name']
        print(c)

        print("**c**")

        # below is relevant!
        channels_data = json_normalize(data=data['data'], record_path='channels', meta='datetime')
        print(channels_data['name'][0], channels_data['value'][0])

    print("****r****")
    r = pd.read_json(data_norm['channels'].to_json(), orient='records', typ='series', convert_axes=False)
    print(r)
    # print(channels_data['channels'])


if __name__ == '__main__':
    getStationDailyData(43, file_name="tec_")
    #getStationMonthlyData(43, file_name="aug")
    #getStationDailyDataForDate(43, year=2018, month=12, day=23, file_name="day")
    #getStationMonthlyDataForMonth(43, year=2019, month=7, file_name="july")
    #getStationRangeData(43, 2018, 6, 1, 2018, 12, 31, file_name='secHalf')
    #getStations(file_name='all_')
    features = getChannelIds()
    print(features.keys())
    print(list(features))
    print(features.values())
    id, times, channels, msrmnts = getChannelsDataFromJSON(file_name='july_2019-7.json')
    #print(features)
    print("*******id******")
    #print(id)
    print("*******times******")
    #print(times)
    print("*******channels******")
    #print(channels)
    print("*******dataFrames****")
    datafs = createDataFrame(file_name='tec__daily.json')
    #print(type(datafs))
    print(datafs)
    #tests()
