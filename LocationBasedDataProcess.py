from DataProcess import *
from collections import OrderedDict

def getStationsData(stations_file_name='stations_data.json'):
    """
    Reads stations information file obtained from API.
    :return: Stations information.
    """
    with open('./data/' + stations_file_name, 'r') as stations_file:
        data = json.load(stations_file)
    return data


def getStationsLocations():
    """
    Finds station location for all stations.
    :return: list of locations.
    """
    data = getStationsData()
    locations = {station['stationId']:[station['location']['latitude'], station['location']['longitude']] for station in data if station['active'] is True and station['location']['latitude'] is not None and station['location']['longitude'] is not None}
    return locations


def calcEuclidianDistance(location1, location2):
    distances_list = [(s1 - s2) ** 2 for s1, s2 in zip(location1, location2)]
    return sum(distances_list) ** 0.5


def getClosestKStationsToLocation(location=None, k=5, station=-1):
    """
    Calculates what are the k closest stations to specific location
    :param location: Coordination.
    :param k: Number of stations to search for.
    :param station: -1 if location is wanted, else station id numer.
    :return: Ordered dictionary of station_id as key and distance as value.
    """
    stations_locations = getStationsLocations()
    base_location = location if station == -1 else stations_locations[station]
    distances = {station_id: calcEuclidianDistance(base_location, stations_locations[station_id]) for station_id in stations_locations}
    ordered_distances = OrderedDict(sorted(distances.items(), key=lambda t: t[1]))
    k_closest_locations = list(zip(ordered_distances.keys(), ordered_distances.values()))[:k+1]
    return dict(k_closest_locations)


def mergeKStationsDataSets(datasets={}):
    """
    Merging datasets of several stations into one dataset.
    :param datasets: Dictionary with station_id as key and dataset as value.
    :return: Merged dataset, where features are followd by _<station_id>
    """
    #Change datasets col names
    datasets_copy = {station_id: dataset.copy(deep=True) for station_id, dataset in datasets.items()}
    items = datasets_copy.items()
    for station_id, station_dataset in datasets_copy.items():
        new_col_names = ['{}_{}'.format(col_name, station_id) for col_name in station_dataset.columns]
        station_dataset.columns = new_col_names
    merge_dataset = pd.concat(list(datasets_copy.values()), axis=1)
    return merge_dataset


def prep_1(file_name_dates):
    """
    Create data sets for the closest stations to the technion.
    """
    # Get technion 10 closest stations data.

    locations = getStationsLocations()
    closest = getClosestKStationsToLocation(locations[43], k=10) # using location
    data_frames = {}
    for station in closest:
        file_name = str(station) + '/' + file_name_dates + '.json'
        print(file_name)
        data_frames[station] = createDataFrame(file_name)
        #exported data_set for faster loading.
        data_frames[station].to_csv('./data/{}/dataset_{}.csv'.format(station, file_name_dates))
    return True


def prep_2():
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


def prep_3():
    """
    check for the technion what are the best k stations around it that improve the results.
    """
    #Starts with the technion itself, and then adding one station at a time.
    merged_datasets = []
    for k in range(11):
        print('k={}'.format(k))
        closest_ids = getClosestKStationsToLocation(station=43, k=k).keys()  # using station
        datasets={}
        for station_id in closest_ids:
            dfcolumns = pd.read_csv('./data/{}/dataset_2019-8.csv'.format(station_id), nrows=1)
            datasets[station_id] = pd.read_csv('./data/{}/dataset_2019-8.csv'.format(station_id), index_col=[0],
                                               usecols=list(range(len(dfcolumns.columns))))
        merged = mergeKStationsDataSets(datasets)
        merged_datasets.append(merged)
        merged.to_csv('./data/43/merged_{}.csv'.format(k))


def create_data_for_all_stations(raw_data_dates, year_b, month_b, day_b, year_e, month_e, day_e, retrieve_data=True):
    stations = getStationsLocations()
    not_in_st = [35, 89, 99, 115, 257, 265, 270]  # Problematic stations.
    data = {}
    for station in stations.keys():
        if (station not in not_in_st and retrieve_data is False) or (station not in not_in_st and station < 115):  # data already exists and no need to withdraw it.
            dfcolumns = pd.read_csv('./data/{}/dataset_{}.csv'.format(station, raw_data_dates), nrows=1)
            data[station] = pd.read_csv('./data/{}/dataset_{}.csv'.format(station, raw_data_dates), index_col=[0], usecols=list(range(len(dfcolumns.columns))))
        if (station not in not_in_st and retrieve_data is True) or (station not in not_in_st and station >= 115):  # need to withdraw data
            file_name = str(station) + '/_{}.json'.format(raw_data_dates)
            print(file_name)
            if retrieve_data is True:
                getStationRangeData(station, year_b, month_b, day_b, year_e, month_e, day_e) # # get data from server.
            data[station] = createDataFrame(file_name)
            # exported data_set for faster loading.
            data[station].to_csv('./data/{}/dataset_{}.csv'.format(station, raw_data_dates))
    merged = mergeKStationsDataSets(data)
    merged.to_csv('./data/merged_all_{}.csv'.format(raw_data_dates))


def locations_main_runner():
    """
    Will be the runner for all experiments functions
    """
    #data = getStationsData()
    # prep_1('_2019-8')
    # prep_2()
    # prep_3()
    create_data_for_all_stations('2016-1-1-2019-10-1', 2016, 1, 1, 2019, 10, 1)
    return True

if __name__ == '__main__':
    locations_main_runner()