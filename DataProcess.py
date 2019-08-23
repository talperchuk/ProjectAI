from datetime import datetime, timedelta
import time
from collections import namedtuple
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
import json
import statsmodels.api as sm
import seaborn as sns
from DataRetrival import *
from GetChannels import getChannelIds
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, median_absolute_error

format = "%Y-%m-%d"

directions = ['North', 'North-West', 'West', 'South-West', 'South', 'South-East', 'East', 'North-East']

def setWDForOHE(df):
    wd_feature = df.WD.tolist()
    for i in range(len(wd_feature)):
        if wd_feature[i] == 0 or wd_feature[i] == 360:
            wd_feature[i] = 'East'
        elif 0 < wd_feature[i] < 90:
            wd_feature[i] = 'North-East'
        elif wd_feature[i] == 90:
            wd_feature[i] = 'North'
        elif 90 < wd_feature[i] < 180:
            wd_feature[i] = 'North-West'
        elif wd_feature[i] == 180:
            wd_feature[i] = 'West'
        elif 180 < wd_feature[i] < 270:
            wd_feature[i] = 'South-West'
        elif wd_feature[i] == 270:
            wd_feature[i] = 'South'
        elif 270 < wd_feature[i] < 360:
            wd_feature[i] = 'South-East'
        else:
            wd_feature[i] = 'Fail'#need to fix this, find a solution for NaNs
    return wd_feature


def setOHEToDF(df, wd_feature):
    df.drop('WD', axis=1, inplace=True)
    df.insert(len(df.columns), "WD", wd_feature, True)
    dummies = pd.get_dummies(df.WD)
    res = pd.concat([df, dummies], axis='columns')
    res.drop('WD', axis=1, inplace=True)
    complement_direction = list(set(directions) - set(wd_feature))
    complement_direction_zero = np.zeros((res.shape[0], len(complement_direction)), dtype=int)
    complement_direction_df = pd.DataFrame(complement_direction_zero, index=res.index, columns=complement_direction)
    df_after_ohe = pd.concat([res, complement_direction_df], axis='columns')
    return df_after_ohe

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
    returned_df = pd.DataFrame(data_frames_per_day).transpose()
    wd_feature = setWDForOHE(returned_df)
    returned_df = setOHEToDF(returned_df, wd_feature)
    returned_df.to_csv('./data/df_with_wind_directions.csv')
    return returned_df


def addPreviousDaysPerFeature(data_frame, feature, amount=1):
    rows_size = data_frame.shape[0]
    new_column = [np.NaN] * amount
    new_column = new_column + [data_frame[feature][i-amount] for i in range(amount, rows_size)]
    new_column_name = "{}_{}".format(feature, amount)
    data_frame[new_column_name] = new_column


def addPreviousDaysFeatures(data_frame, amount=1):
    features = list(data_frame)
    for feature in features:
        for i in range(1, amount):
            addPreviousDaysPerFeature(data_frame, feature, i)


def getCorrelationOfDataForFeature(data_frame, feature):
    correlations = data_frame.corr()[[feature]].sort_values(feature)
    predicators = [feature_legal for feature_legal in correlations.index if (abs(correlations[feature][feature_legal]) > 0.6)]
    predicators.remove('TD')
    return correlations, predicators


def createRelationOfFeaturesToFeatureGraphs(data_frame, main_feature, predicators, reshape_x, reshape_y):
    new_dataframe = data_frame[[main_feature] + predicators]
    plt.rcParams['figure.figsize'] = [16, 22]
    fig, axes = plt.subplots(nrows=reshape_x, ncols=reshape_y, sharey=True)
    #arr = np.array(predicators).reshape(reshape_x, reshape_y)
    arr = np.array(predicators)
    for row, col_arr in enumerate(arr):
        for col, feature in enumerate(col_arr):
            print("**df2[feature] is: {}\n{}".format(feature, new_dataframe[feature]))
            axes[row, col].scatter(new_dataframe[feature], new_dataframe[main_feature])
            if col == 0:
                axes[row, col].set(xlabel=feature, ylabel=main_feature)
            else:
                axes[row, col].set(xlabel=feature)
    # testing this function for failure.
    plt.show()


def createHeatMap(data_frame, features=[]):
    data_frame_features = list(data_frame) if features == [] else features
    data_frame_selected = data_frame[data_frame_features]
    plt.figure(figsize=(12, 10))
    sns.heatmap(data_frame_selected.corr(), annot=True, cmap=plt.cm.Blues)
    plt.show()


def getModelFeatures(data_frame, predictors, feature):
    x = data_frame[predictors]
    y = data_frame[feature]
    x = sm.add_constant(x)
    alpha = 0.05 # TODO: HYPER PARAM

    model = sm.OLS(y, x, missing='drop').fit()
    while not model.pvalues.empty:
        p_values = model.pvalues
        max_index = p_values.idxmax()
        if p_values[max_index] > alpha:
            x = x.drop(max_index, axis=1)
        else:
            break
        model = sm.OLS(y, x, missing='drop').fit()
    print('*****x:')
    print(x)
    print('*****x:')
    print(type(x))
    x = x if 'const' not in x else x.drop('const', axis=1)
    return model, x, y

def predict(x, y):
    test_size = 0.2 # TODO: HYPER PARAM
    random_state = 12 # TODO: HYPER PARAM
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

    regressor = LinearRegression()
    x_train.fillna(x_train.mean(), inplace=True)
    x_test.fillna(x_test.mean(), inplace=True)
    y_train.fillna(y_train.mean(), inplace=True)
    y_test.fillna(y_test.mean(), inplace=True)
    regressor.fit(x_train, y_train)

    prediction = regressor.predict(x_test)
    print("prediction: {}".format(prediction))
    print("The Explained Variance: %.2f" % regressor.score(x_test, y_test))
    print("The Mean Absolute Error: %.2f degrees celsius" % mean_absolute_error(y_test, prediction))
    print("The Median Absolute Error: %.2f degrees celsius" % median_absolute_error(y_test, prediction))
