from datetime import datetime, timedelta
import time
from collections import namedtuple
import pandas as pd
import requests
import matplotlib.pyplot as plt
from DataRetrival import *

features_list = list(getChannelIds())
id, times, channels, msrmnts = getChannelsDataFromJSON(file_name='aug_2019-8.json')

df = pd.DataFrame(msrmnts, columns=features_list)

print(df)