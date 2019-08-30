
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
    #getStationRangeData(36, 2018, 1, 1, 2018, 12, 31, file_name='yotvata')
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
    datafs = createDataFrame(file_name='gamla_2018-1-1-2018-12-31.json')
    #print(type(datafs))
    print(str(datafs))

    features = list(datafs)
    for feature in features:
        for i in range(1, 4):
            addPreviousDaysPerFeature(datafs, feature, i)

    correlations = datafs.corr()[['TD']].sort_values('TD')
    predicators = [feature_legal for feature_legal in correlations.index if (abs(correlations['TD'][feature_legal]) > 0.6)]
    predicators.remove('TD')

    new_dataframe = datafs[['TD'] + predicators]
    new_dataframe.to_csv('./data/new_dataframe csv')

    x = new_dataframe[predicators]
    y = new_dataframe['TD']
    x = sm.add_constant(x)
    #x.insert(loc=0, column='const', value=1.0)
    print('*******************************************************************************')
    print(x)
    alpha = 0.05 # TODO: HYPER PARAM

    model = sm.OLS(y, x, missing='drop').fit()
    while not model.pvalues.empty:
        p_values = model.pvalues
        max_index = p_values.idxmax()
        if p_values[max_index] > alpha:
            print('Max Index is: {}'.format(max_index))
            x = x.drop(max_index, axis=1)
        else:
            break
        model = sm.OLS(y, x, missing='drop').fit()
        print(model.summary())
    print(model.summary())
    print('*****x:')
    print(x)
    print('*****x:')
    print(type(x))
    x = x if 'const' not in x else x.drop('const', axis=1)

    test_size = 0.2 # TODO: HYPER PARAM
    random_state = 12 # TODO: HYPER PARAM
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

    x_train.to_csv('./data/x_trainBeforeFillNA')
    x_test.to_csv('./data/x_testBeforeFillNA')
    y_train.to_csv('./data/y_trainBeforeFillNA')
    y_test.to_csv('./data/y_testBeforeFillNA')

    regressor = LinearRegression()
    x_train = x_train.fillna(x_train.mean())
    x_train.to_csv('./data/x_train csv')
    x_test = x_test.fillna(x_test.mean())
    x_test.to_csv('./data/x_test csv')
    y_train = np.roll(y_train, -1)
    y_train[(len(y_train)-1)] = np.mean(y_train)
    y_train = pd.DataFrame(y_train).fillna(y_train.mean())
    y_train.to_csv('./data/y_train csv')
    y_test = np.roll(y_test, -1)
    y_test[(len(y_test)-1)] = np.mean(y_test)
    y_test = pd.DataFrame(y_test).fillna(y_test.mean())
    y_test.to_csv('./data/y_test csv')
    regressor.fit(x_train, y_train)

    prediction = regressor.predict(x_test)
    print("prediction: {}".format(prediction))
    print('************test*****************')
    print(y_test)
    print("The Explained Variance: %.2f" % regressor.score(x_test, y_test))
    print("The Mean Absolute Error: %.2f degrees celsius" % mean_absolute_error(y_test, prediction))
    print("The Median Absolute Error: %.2f degrees celsius" % median_absolute_error(y_test, prediction))































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
    """""
    # try to classify.
    addPreviousDaysFeatures(datafs, 4)
    print("**corr**")
    corr, pred = getCorrelationOfDataForFeature(datafs, 'TD')

    # predicators = ['NIP', 'NIP_1', 'NIP_2', 'Grad', 'Grad_1', 'Grad_2', 'Grad_3', 'TDmax', 'TDmax_1', 'TDmax_2', 'TDmax_3', 'TDmin', 'TDmin_1', 'TDmin_2', 'TDmin_3', 'TD_1', 'TD_2', 'TD_3']
    new_dataframe = datafs[['TD'] + pred]
    #new_dataframe.to_csv('./data/yotvetaData')
    # createRelationOfFeaturesToFeatureGraphs(datafs, 'TD', predicators, len(pred), 1)
    # createHeatMap(new_dataframe)
    print(pred)
    model, x, y = getModelFeatures(new_dataframe, pred, 'TD')
    predict(x, y)
    """


