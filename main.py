
from pandas.io.json import json_normalize
from DataProcess import *
from LocationBasedDataProcess import *

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
    #getStationDailyData(43, file_name="tec")
    #getStationMonthlyData(43, file_name="aug")
    #getStationDailyDataForDate(43, year=2018, month=12, day=23, file_name="day")
    #getStationMonthlyDataForMonth(43, year=2019, month=8, file_name="")
    #getStationRangeData(36, 2016, 1, 1, 2018, 12, 31, file_name='yotvata')
    #getStations(file_name='all_')
    # # Running Location based Tests. # #
    locations_main_runner()
    # # Get the channels Ids based on one example # #
    #features = getChannelIds()

    #id, times, channels, msrmnts = getChannelsDataFromJSON(file_name='july_2019-7.json')
    #print(features)
    """
    
    # # Create data frame from a json file. # #
    datafs = createDataFrame(file_name='yotvata_july_2019-7.json')

    # # Create heatmap # #
    createHeatMap(datafs)

    # # Add previous days dat as features # #
    print("*******Extended features******")
    addPreviousDaysFeatures(datafs, 4)

    # #calc correlation of each feature with respect to main feature.
    # #calc all features above abs of corr_hyper_param=0.5
    #correlation, predictors = getCorrelationOfDataForFeature(datafs, 'TD', corr_hyper_param=0.5)


    # tests()
    # ### deriving the features
    # # using small dataset for FIRST tries and checks.
    tmp = datafs[['TDmax', 'TDmin', 'TD']]
    print("*******dataFramesInfo****")
    print(tmp.info())
    # # calc the spread based on IQR.
    # # Respect to the part of spread in the article.
    spread = datafs.describe().transpose()
    IQR = spread['75%'] - spread['25%']
    spread['outliers'] = (spread['min'] < (spread['25%']-(3*IQR))) | (spread['max'] > (spread['75%']+3*IQR)) # TODO: add to data process
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
    """

    # try to classify.
    # addPreviousDaysFeatures(datafs, 6)
    print("**corr**")
    # for col in datafs:
    #     mean = datafs[col].mean()
    #     datafs[col].fillna(mean, inplace=True)
    #
    """
    """
    # #First try of predict and fit (manually)
    corr, pred = getCorrelationOfDataForFeature(datafs, 'TD')

    predicators = ['NIP', 'NIP_1', 'NIP_2', 'Grad', 'Grad_1', 'Grad_2', 'Grad_3', 'TDmax', 'TDmax_1', 'TDmax_2', 'TDmax_3', 'TDmin', 'TDmin_1', 'TDmin_2', 'TDmin_3', 'TD_1', 'TD_2', 'TD_3']

    new_dataframe = datafs[['TD'] + pred]

    new_dataframe = new_dataframe.dropna()
    print('********INFO: {}'.format(new_dataframe.info()))
    createRelationOfFeaturesToFeatureGraphs(datafs, 'TD', pred, len(pred), 1)
    createHeatMap(new_dataframe)
    print('********Pred: {}'.format(pred))
    model, x, y = getModelBackElimination(new_dataframe, pred, 'TD')
    print('********Final summary: {}'.format(model.summary()))
    predict(x, y)

    print('********X: {}'.format(x))
    print('********Y: {}'.format(y))

    # Predict addons of multiple days and for changing corr hyper param (4/9/19)
    for day_addon in range(29):
    # try to classify.
        print('DAY: {}!!!!!!!!'.format(day_addon))
        addPreviousDaysFeatures(datafs, day_addon)
        print("**corr**")
        for col in datafs:
            mean = datafs[col].mean()
            datafs[col].fillna(mean, inplace=True)

        for corr_hyper in np.arange(0.1, 1, 0.1):
            print('################################# {} ##########################'.format(corr_hyper))
            corr, pred = getCorrelationOfDataForFeature(datafs, 'TD')
            new_dataframe = datafs[['TD'] + pred]
            model, x, y = getModelBackElimination(new_dataframe, pred, 'TD')
            ('********Final summary: {}'.format(model.summary()))
            predict(x, y)
    """
