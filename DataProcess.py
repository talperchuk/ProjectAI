from datetime import datetime, timedelta
import time
from collections import namedtuple
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
import json
from DataRetrival import *
from GetChannels import getChannelIds

format = "%Y-%m-%d"


def getChannelsDataFromJSON(file_name='dailyTarget.json'):
    with open('./data/' + file_name, 'r') as f:
        data = json.load(f)
    station_id = data['stationId']
    data_as_str = json.dumps(data['data'])
    data_pd = pd.read_json(data_as_str, orient='records', typ='series')
    measurments_summary = {}
    measurment_times = []
    for measurment in data_pd:
        measurment_channels = {}
        measurment_times.append(measurment['datetime'])
        measurment_channels['datetime'] = (measurment['datetime'])
        channels = measurment['channels']
        for channel in channels:
            channel_value = channel['value'] if channel['valid'] is True else np.NaN
            if channel['name'] in measurment_channels:
                measurment_channels[channel['name']].append(channel_value)
            else:
                measurment_channels[channel['name']] = [channel_value]
        measurments_summary[measurment['datetime']] = measurment_channels
    return station_id, measurment_times, measurment_channels, measurments_summary


def createDataFrame(file_name):
    features_list = list(getChannelIds())
    features_list.append('datetime')
    id, times, channels, measurements = getChannelsDataFromJSON(file_name=file_name)
    measurement_data_frame = pd.DataFrame()
    data_frames_per_day = {}
    for measurement in measurements:
        measurement_time = time.strptime(measurement.split("T")[0], format)
        if measurement_time not in data_frames_per_day:
            measurement_data_frame = pd.DataFrame()
        df = pd.DataFrame(measurements[measurement], columns=features_list).set_index('datetime')
        measurement_data_frame = measurement_data_frame.append(df)
        data_frames_per_day[measurement_time] = measurement_data_frame  # can reduce times by less insertions.
    for frame in data_frames_per_day:
        data_frames_per_day[frame] = data_frames_per_day[frame].mean(axis=0)
    return pd.DataFrame(data_frames_per_day).transpose()
