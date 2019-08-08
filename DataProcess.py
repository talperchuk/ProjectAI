from datetime import datetime, timedelta
import time
from collections import namedtuple
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
from DataRetrival import *

format = "%Y-%m-%d"

def createDataFrame(file_name):
    features_list = list(getChannelIds())
    features_list.append('datetime')
    id, times, channels, msrmnts = getChannelsDataFromJSON(file_name=file_name)
    t = time.strptime(times[0].split("T")[0], format)
    tmp = pd.DataFrame()
    data_frames_per_day = {}
    for x in msrmnts:
        x_t = time.strptime(x.split("T")[0], format)
        if (x_t  not in data_frames_per_day):
            tmp = pd.DataFrame()
        df = pd.DataFrame(msrmnts[x], columns=features_list).set_index('datetime')
        tmp = tmp.append(df)
        data_frames_per_day[x_t] = tmp  # can reduce times by less insertions.
    return data_frames_per_day
