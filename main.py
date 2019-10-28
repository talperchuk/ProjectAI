
from pandas.io.json import json_normalize
from DataProcess import *
from LocationBasedDataProcess import *
from findFeaturesScript import find_features_runner


if __name__ == '__main__':
    """TMP
    ############### Retrieve data from the meteorological institute. ###############
    # File named stations_information.json located in data/ will be created.
    getStations(file_name='stations_information')
    # File named _daily.json located in data/43/ will be created
    getStationDailyData(station=22)
    # File named xmpl_monthly.json located in data/43/ will be created
    getStationMonthlyData(station=22, file_name='xmpl')
    # File named _2019_10_1.json located in data/43/ will be created
    getStationDailyDataForDate(station=22, day=1, month=10, year=2019)
    # File named _2019_10.json located in data/43/ will be created
    getStationMonthlyDataForMonth(station=22, month=10, year=2019)
    # File named _2019-9-20-2019-10-1.json located in data/43/ will be created
    getStationRangeData(22, 2019, 9, 1, 2019, 10, 5)
    
    ############### Retrieve data for specific channel from the meteorological institute. ###############
    ids = getChannelIds()
    # File named _daily.json located in data/43/ will be created contains only  data for TD channel.
    #getStationDailyData(station=22, channel=ids['TD'], file_name='channel_TD')

    ############### Data Frame Creation ###############
    file_name = '2019-9-1-2019-10-5'
    # Data frame will be created from data/43/_2019-9-20-2019-10-1.json
    technion_final_test_dataframe = createDataFrame(file_name='{}/_{}.json'.format(22, file_name))
    #  Export data frame to csv.
    technion_final_test_dataframe.to_csv('./data/{}/dataset_{}.csv'.format(22, file_name))
    
    ############## All Stations Merged Data Frame Creation ###############
    # File named merged_all_2019-7-1-2019-9-1.csv located in data/ will be created.
    create_data_for_all_stations('2019-7-1-2019-9-1', 2019, 7, 1, 2019, 9, 1)
    TMP"""
    ############## Finding Best parameters for each regressor  ###############
    # Can also be run using terminal - just run fundFeaturesScript.py.
    find_features_runner(raw_data_file_name="./data/22/dataset_2019-9-1-2019-10-5.csv",
                         output_path_name='station22_test',
                         output_file_name='regression_station22_{}.csv'.format('2019-9-1-2019-10-5'),
                         using_merged=False)

    """ 
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UNKNOWN!!!!!!!!! ->
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
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UNKNOWN!!!!!!!!!  <-
    """



