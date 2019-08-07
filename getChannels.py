import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

#data of specific time measurment.
data = [{"id": 1, "name": "WSmax", "alias": 0, "value": 2.1, "status": 2, "valid": False, "description": 0},
        {"id": 2, "name": "WDmax", "alias": 0, "value": 302.0, "status": 2, "valid": False, "description": 0}, 
        {"id": 3, "name": "WS", "alias": 0, "value": 1.2, "status": 2, "valid": False, "description": 0}, 
        {"id": 4, "name": "WD", "alias": 0, "value": 267.0, "status": 2, "valid": False, "description": 0}, 
        {"id": 5, "name": "STDwd", "alias": 0, "value": 28.5, "status": 2, "valid": False, "description": 0}, 
        {"id": 6, "name": "TD", "alias": 0, "value": 25.2, "status": 1, "valid": True, "description": 0}, 
        {"id": 7, "name": "RH", "alias": 0, "value": 70.0, "status": 1, "valid": True, "description": 0}, 
        {"id": 8, "name": "TDmax", "alias": 0, "value": 25.2, "status": 1, "valid": True, "description": 0}, 
        {"id": 9, "name": "TDmin", "alias": 0, "value": 25.1, "status": 1, "valid": True, "description": 0}, 
        {"id": 10, "name": "Grad", "alias": 0, "value": 0.0, "status": 1, "valid": True, "description": 0}, 
        {"id": 11, "name": "NIP", "alias": 0, "value": 2.0, "status": 1, "valid": True, "description": 0}, 
        {"id": 12, "name": "DiffR", "alias": 0, "value": 1.0, "status": 1, "valid": True, "description": 0}, 
        {"id": 13, "name": "WS1mm", "alias": 0, "value": 1.6, "status": 2, "valid": False, "description": 0}, 
        {"id": 15, "name": "Ws10mm", "alias": 0, "value": 1.8, "status": 2, "valid": False, "description": 0}, 
        {"id": 16, "name": "Time", "alias": 0, "value": 2.0, "status": 2, "valid": False, "description": 0}, 
        {"id": 20, "name": "Rain", "alias": 0, "value": 0.0, "status": 1, "valid": True, "description": 0}]

def getChannelIds():
    res = {}
    for row in data:
        res[row["name"]] = row["id"]
    #print(res)
    return res

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


