from DataProcess import *
from DataRetrival import *
from findFeaturesScript import *

def prepareDatasetWithAddingDays(merged_raw_data_file_name, max_days_added=30):
    datafs = pd.read_csv(merged_raw_data_file_name)
    datafs.drop(labels='Unnamed: 0', axis=1, inplace=True)
    addPreviousDaysFeatures(datafs, max_days_added)
    for col in datafs:
        mean = datafs[col].mean()
        datafs[col].fillna(mean, inplace=True)
    return datafs

def fromStringToList(str):
    str = str.replace('[', '')
    str = str.replace(']', '')
    str = str.replace('\\', '')
    str = str.replace('\'', '')
    str = str.replace(' ', '')
    #str = str.replace('0', '')
    str = str.replace('...', '')
    str = str.split(',')
    return str


regressions = {
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'ElasticNet': ElasticNet(),
    'SVR': SVR(),
    'MLPRegression': MLPRegressor(),
    'RFR': RandomForestRegressor(),
}

param_grid = {
    'Ridge': [{
        'alpha': np.linspace(0.1, 5.0, 25),
    }],
    'Lasso': [{
        'alpha': np.linspace(0.1, 5.0, 25),
    }],
    'ElasticNet': [{
        'alpha': np.linspace(0.1, 5.0, 25),
        'l1_ratio': [0.25, 0.5, 0.75],
    }],
    'SVR': [{
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
        'C': [0.01, 0.1, 1, 10, 100],
    }],
    'MLPRegression': [{
        'activation': ['identity', 'logistic', 'tanh', 'relu'],
        'solver': ['lbfgs', 'adam'],
        'alpha': [0.000001, 0.00001, 0.0001, 0.001, 0.01],
    }],
    'RFR': [{
        'n_estimators': [10, 20, 30, 40, 50],
        'criterion': ['mse', 'mae'],
        'min_samples_split': [2, 3, 4, 5, 6, 7, 8, 9],
        'min_samples_leaf': [2, 3, 4, 5, 6, 7, 8, 9],
    }],
}

feature_regressions_map = {
    'Ridge': pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/best_features/best_features_Ridge.csv")['Features'],
    'Lasso': pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/best_features/best_features_Lasso.csv")['Features'],
    'ElasticNet': pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/best_features/best_features_ElasticNet.csv")['Features'],
    'SVR': pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/best_features/best_features_SVR.csv")['Features'],
    'MLPRegression': pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/best_features/best_features_MLPRegression.csv")['Features'],
    'RFR': pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/best_features/best_features_RFR.csv")['Features'],
}

mean_absolute_error_scorer = make_scorer(mean_absolute_error)

checked_station = 43

if __name__ == '__main__':
    start = str(datetime.now())
    # Create path folders if needed
    path = './data/Experiments/station_43_1_years_all_stations_submit_test/best_features'
    path_results = path + '/grid_search_resultes/'
    #pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(path_results).mkdir(parents=True, exist_ok=True)
    print('created')
    #full_data_set = pd.read_csv("./data/Experiments/station_43_1_years_all_stations_submit_test/regression_all_stations_dataset_1_years.csv") #!!
    #full_data_set.drop(labels='Unnamed: 0', axis=1, inplace=True)
    full_data_set = prepareDatasetWithAddingDays(merged_raw_data_file_name='./data/merged_all_2019-4-1-2019-6-20.csv', max_days_added=30)
    y_train = full_data_set['TD_{}'.format(checked_station)]
    y_train = np.roll(y_train, -1)
    y_train[(len(y_train) - 1)] = np.mean(y_train)
    y_train = pd.DataFrame(y_train, columns=['TD_{}_tomorrow'.format(checked_station)]).fillna(y_train.mean())
    for key in regressions:
        list_of_best_features = fromStringToList(feature_regressions_map[key].values[0])
        x_train = full_data_set[list_of_best_features]
        grid_search_reg = GridSearchCV(regressions[key], param_grid[key],
                                       scoring=mean_absolute_error_scorer, cv=10, verbose=5)
        grid_search_reg.fit(x_train, y_train)
        pd.DataFrame(grid_search_reg.cv_results_).to_csv(path_results + key + '.csv')

    end = str(datetime.now())
    print("Starts experiment at: {}".format(start))
    print("End experiment at: {}".format(end))


