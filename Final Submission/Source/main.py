
from pandas.io.json import json_normalize
from DataProcess import *
from LocationBasedDataProcess import *
from findFeaturesScript import find_features_runner
from mainScript import main_script_runner


if __name__ == '__main__':

    ############### Retrieve data from the meteorological institute. ###############
    # File named stations_information.json located in data/ will be created.
    getStations(file_name='stations_information')
    # File named _daily.json located in data/22/ will be created
    getStationDailyData(station=22)
    # File named xmpl_monthly.json located in data/22/ will be created
    getStationMonthlyData(station=22, file_name='xmpl')
    # File named _2019_10_1.json located in data/22/ will be created
    getStationDailyDataForDate(station=22, day=1, month=10, year=2019)
    # File named _2019_10.json located in data/22/ will be created
    getStationMonthlyDataForMonth(station=22, month=10, year=2019)
    # File named _2016-1-1-2019-10-1.json located in data/22/ will be created
    getStationRangeData(22, 2016, 1, 1, 2019, 10, 1)
    
    ############### Retrieve data for specific channel from the meteorological institute. ###############
    ids = getChannelIds()
    # File named _daily.json located in data/22/ will be created contains only  data for TD channel.
    getStationDailyData(station=22, channel=ids['TD'], file_name='channel_TD')

    ############### Data Frame Creation ###############
    file_name = '2016-1-1-2019-10-1'
    # Data frame will be created from data/22/_2016-1-1-2019-10-1.json
    technion_final_test_dataframe = createDataFrame(file_name='{}/_{}.json'.format(22, file_name))
    #  Export data frame to csv.
    technion_final_test_dataframe.to_csv('./data/{}/dataset_{}.csv'.format(22, file_name))

    ############## All Stations Merged Data Frame Creation ###############
    # File named merged_all_2016-1-1-2019-10-1.csv located in data/ will be created.
    create_data_for_all_stations('2016-1-1-2019-10-1', 2016, 1, 1, 2019, 10, 1)

    ############## Finding all parameters combinations for each regressor  ###############
    # Can also be run using terminal - just run fundFeaturesScript.py.
    find_features_runner(raw_data_file_name="./data/merged_all_2016-1-1-2019-10-1.csv",
                         output_path_name='merged_path_exmpl',
                         output_file_name='regression_all_stations_dataset_2016-1-1-2019-10-1.csv',
                         using_merged=True)
    
    ############## Finding best properties for each regressor based on best parameters ###############
    main_script_runner(raw_data_file_name='./data/merged_all_2016-1-1-2019-10-1.csv', using_merged=True)




