import requests
import json
import pandas as pd

#data of specific time measurment used for getting channels ids.
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
    return res

