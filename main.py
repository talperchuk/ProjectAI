
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
    datafs = createDataFrame(file_name='secHalf_2018-6-1-2018-12-31.json')
    #print(type(datafs))
    print(datafs)
    print("*******Extended features******")
    predicators = ['NIP', 'NIP_2', 'NIP_1', 'NIP_3', 'Grad_3', 'Grad', 'Grad_2', 'Grad_1', 'TDmax_3', 'TD_3', 'TDmin_3', 'TDmax_2', 'TD_2', 'TDmin_2', 'TDmax_1', 'TD_1', 'TDmin_1', 'TDmax' ]
    addPreviousDaysFeatures(datafs, 4)
    # calc correlation
    #print(datafs.corr()[['TD']].sort_values('TD'))
    df2 = datafs[['TD'] + predicators]
    #create corr graphs
    """below graphs shows the lineariti of """
    plt.rcParams['figure.figsize'] = [16, 22]
    fig, axes = plt.subplots(nrows=6, ncols=3, sharey=True)
    arr = np.array(predicators).reshape(6, 3)
    for row, col_arr in enumerate(arr):
        for col, feature in enumerate(col_arr):
            print("**df2[feature] is: {}\n{}".format(feature, df2[feature]))
            axes[row, col].scatter(df2[feature], df2['TD'])
            if col == 0:
                axes[row, col].set(xlabel=feature, ylabel='TD')
            else:
                axes[row, col].set(xlabel=feature)
    plt.show()
    #tests()
    #### deriving the features
    """
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
