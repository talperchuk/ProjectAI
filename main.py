
from pandas.io.json import json_normalize
from DataProcess import *

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
    #getStationDailyData(43, file_name="tec_")
    #getStationMonthlyData(43, file_name="aug")
    #getStationDailyDataForDate(43, year=2018, month=12, day=23, file_name="day")
    #getStationMonthlyDataForMonth(43, year=2019, month=7, file_name="july")
    #getStationRangeData(36, 2016, 1, 1, 2018, 12, 31, file_name='yotvata')
    #getStations(file_name='all_')
    features = getChannelIds()
    print(features.keys())
    print(list(features))
    print(features.values())
    #id, times, channels, msrmnts = getChannelsDataFromJSON(file_name='july_2019-7.json')
    #print(features)
    print("*******id******")
    #print(id)
    print("*******times******")
    #print(times)
    print("*******channels******")
    #print(channels)
    print("*******dataFrames****")
    datafs = createDataFrame(file_name='yotvata_2016-1-1-2018-12-31.json')
    #print(type(datafs))
    #print(str(datafs))
    #heatmap
    """
    createHeatMap(datafs)

    print("*******Extended features******")
    predicators = ['NIP', 'NIP_1', 'NIP_2', 'Grad', 'Grad_1', 'Grad_2', 'Grad_3', 'TDmax', 'TDmax_1', 'TDmax_2', 'TDmax_3', 'TDmin', 'TDmin_1', 'TDmin_2', 'TDmin_3', 'TD_1', 'TD_2', 'TD_3']
    addPreviousDaysFeatures(datafs, 4)
    # calc correlation
    print(getCorrelationOfDataForFeature(datafs, 'TD'))
    #creating correlation graphs
    createRelationOfFeaturesToFeatureGraphs(datafs, 'TD', predicators, 6, 3)

    #tests()
    #### deriving the features
    tmp = datafs[['TDmax', 'TDmin', 'TD']]
    print("*******dataFramesInfo****")
    print(tmp.info())
    spread = datafs.describe().transpose()
    IQR = spread['75%'] - spread['25%']
    spread['outliers'] = (spread['min'] < (spread['25%']-(3*IQR))) | (spread['max'] > (spread['75%']+3*IQR))
    print('*******dataFramesSpread****')
    print(spread)
    print(spread.info())
    print('*******dataFramesOutliers****')
    print(spread.ix[spread.outliers])
    print('*******dataFramesDropna****')
    datafs = datafs.dropna()
    print(datafs)
    N = 2
    feature = 'TDmin'
    rows = tmp.shape[0]
    plt.rcParams['figure.figsize'] = [14, 8]
    tmp.TDmin.hist()
    plt.title('Distribution of TDmin')
    plt.xlabel('TDmin')
    plt.show()
    """

    # try to classify.
    addPreviousDaysFeatures(datafs, 6)
    print("**corr**")
    corr, pred = getCorrelationOfDataForFeature(datafs, 'TD')

    # predicators = ['NIP', 'NIP_1', 'NIP_2', 'Grad', 'Grad_1', 'Grad_2', 'Grad_3', 'TDmax', 'TDmax_1', 'TDmax_2', 'TDmax_3', 'TDmin', 'TDmin_1', 'TDmin_2', 'TDmin_3', 'TD_1', 'TD_2', 'TD_3']

    new_dataframe = datafs[['TD'] + pred]
    new_dataframe = new_dataframe.dropna()
    print('********INFO: {}'.format(new_dataframe.info()))
    # createRelationOfFeaturesToFeatureGraphs(datafs, 'TD', predicators, len(pred), 1)
    createHeatMap(new_dataframe)
    print('********Pred: {}'.format(pred))
    model, x, y = getModelBackElimination(new_dataframe, pred, 'TD')
    print('********Final summary: {}'.format(model.summary()))
    predict(x, y)
    print('********X: {}'.format(x))
    print('********Y: {}'.format(y))
