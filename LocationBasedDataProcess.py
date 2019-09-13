from DataProcess import *
from collections import OrderedDict

def getStationsData(stations_file_name='stations_data.json'):
    with open('./data/' + stations_file_name, 'r') as stations_file:
        data = json.load(stations_file)
    return data


def getStationsLocations():
    data = getStationsData()
    locations = {station['stationId']:[station['location']['latitude'], station['location']['longitude']] for station in data if station['active'] is True and station['location']['latitude'] is not None and station['location']['longitude'] is not None}
    return locations


def calcEuclidianDistance(location1, location2):
    distances_list = [(s1 - s2) ** 2 for s1, s2 in zip(location1, location2)]
    return sum(distances_list) ** 0.5


def getClosestKStationsToLocation(location, k=5, station=-1):
    stations_locations = getStationsLocations()
    base_location = location if station == -1 else stations_locations[station]
    distances = {station_id: calcEuclidianDistance(base_location, stations_locations[station_id]) for station_id in stations_locations if station_id != station and base_location != stations_locations[station_id]}
    ordered_distances = OrderedDict(sorted(distances.items(), key=lambda t: t[1]))
    k_closest_locations = list(zip(ordered_distances.keys(), ordered_distances.values()))[:k]
    return dict(k_closest_locations)


def mergeKStationsDataSets(datasets={}):
    #Change datasets col names
    datasets_copy = {station_id: dataset.copy(deep=True) for station_id, dataset in datasets.items()}
    items = datasets_copy.items()
    for station_id, station_dataset in datasets_copy.items():
        new_col_names = ['{}_{}'.format(col_name, station_id) for col_name in station_dataset.columns]
        station_dataset.columns = new_col_names
    merge_dataset = pd.concat(list(datasets_copy.values()), axis=1)
    return merge_dataset


def expr_1():
    """
    Create data sets for the closest stations to the technion.
    """
    # Get technion 10 closest stations data.
    #technion_10_neighbors = [42, 41, 44, 78, 67, 186, 45, 343, 205, 16]
    # for station in technion_10_neighbors:
    #     getStationMonthlyDataForMonth(station=station, month=8, year=2019)
    locations = getStationsLocations()
    closest = getClosestKStationsToLocation(locations[43], k=10) # using location
    data_frames = {}
    for station in closest:
        file_name = str(station) + '/_2019-8.json'
        print(file_name)
        data_frames[station] = createDataFrame(file_name)
        #exported data_set for faster loading.
        data_frames[station].to_csv('./data/{}/dataset_2019-8.csv'.format(station))
    return True


def expr_2():
    '''
    Get dataframe of technion closest 10 locations (without the technion itself)
    ----AFTER: Changed get closest to include the base station itself due to the fact that it is needed.
    '''
    technion_10_neighbors = [42, 41, 44, 78, 67, 186, 45, 343, 205, 16]
    datasets = {}
    for station_id in technion_10_neighbors:
        dfcolumns = pd.read_csv('./data/{}/dataset_2019-8.csv'.format(station_id), nrows=1)
        datasets[station_id] = pd.read_csv('./data/{}/dataset_2019-8.csv'.format(station_id), index_col=[0], usecols=list(range(len(dfcolumns.columns))))
    merged = mergeKStationsDataSets(datasets)
    merged.to_csv('./data/merged.csv')


def expr_3():
    """
    check for the technion what are the best k stations around it that improve the results.
    """
    # create technion data frame
    file_name = str(43) + '/_2019-8.json'
    print(file_name)
    tec_dataframe = createDataFrame(file_name)
    tec_dataframe.to_csv('./data/{}/dataset_2019-8.csv'.format(43))

    # Get the locations of all stations.
    locations = getStationsLocations()

    #Starts with the technion itself, and then adding one station at a time.
    merged_datasets = []
    for k in range(11):
        closest_ids = getClosestKStationsToLocation(station=43, k=k).keys()  # using station
        datasets={43: tec_dataframe}
        for station_id in closest_ids:
            dfcolumns = pd.read_csv('./data/{}/dataset_2019-8.csv'.format(station_id), nrows=1)
            datasets[station_id] = pd.read_csv('./data/{}/dataset_2019-8.csv'.format(station_id), index_col=[0],
                                               usecols=list(range(len(dfcolumns.columns))))






def locations_main_runner():
    """
    Will be the runner for all experiments functions
    """
    #data = getStationsData()
    expr_1()
    expr_2()
    return True
