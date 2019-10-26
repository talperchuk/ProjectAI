from pandas.io.json import json_normalize
import csv
import numpy as np
from DataProcess import *
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import *
from datetime import datetime
from statistics import mean
import sklearn.metrics
import matplotlib.pyplot as plt


def find_features_runner(raw_data_file_name, output_path_name, output_file_name):
    datafs = pd.read_csv(raw_data_file_name)

    ###########################Global Parameters###########################
    missing_threshold = 0.25
    days = [0, 5, 10, 20, 25, 30]
    corr_hyper_params = np.array(list(np.arange(0, 0.5, 0.1)))
    select_k_best = [5, 20, 40, 60, 80, 100]

    ###########################Chosen Station###########################
    checked_station = 43

    ######Add this if reading from "merged" files#####################
    ######Drop missing columns with thrashold over missing_threshold value#######
    datafs.drop(labels='Unnamed: 0', axis=1, inplace=True)

    ###########################Create working folder#################################
    path = './data/Experiments/station_{}_{}/'.format(checked_station, output_path_name)
    result_file_name = path + output_file_name
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    ###########################Script#################################
    data_frame = datafs.copy(deep=True)

    with open(result_file_name, 'w', newline='') as file:
        field_names = ['Days', 'Corr', 'K_best', 'Reg', 'Features', 'Mean absolute error']
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        for day in days:
            print('Added {} days'.format(day))
            addPreviousDaysFeatures(data_frame, day)
            for col in data_frame:
                mean = data_frame[col].mean()
                data_frame[col].fillna(mean, inplace=True)
            # # If not working on merged file, use 'TD' instead of 'TD_{}' in all places above. # #
            for corr_hyper_param in corr_hyper_params:
                label = data_frame['TD_{}'.format(checked_station)]
                label = np.roll(label, -1)
                label[(len(label) - 1)] = np.mean(label)
                label = pd.DataFrame(label, columns=['TD_{}_tomorrow'.format(checked_station)]).fillna(label.mean())
                new_data_frame = pd.concat([data_frame, label], axis=1)
                correlations, predicators = getCorrelationOfDataForFeature(new_data_frame,
                                                                           'TD_{}_tomorrow'.format(checked_station),
                                                                           corr_hyper_param)
                finale_data_frame = new_data_frame[predicators]
                for select_k_hyper_param in select_k_best:
                    for reg in [Ridge(), Lasso(), ElasticNet(), SVR(), MLPRegressor(), RandomForestRegressor()]:
                        x = finale_data_frame
                        y = label

                        x_selected = []
                        k = min(select_k_hyper_param, x.shape[1])
                        if select_k_hyper_param != x.shape[1] and k == select_k_hyper_param:
                            selected_features = SelectKBest(f_regression, k=k).fit(x, y)
                            indices_features = selected_features.get_support(indices=True)
                            x_selected = [x.columns[i] for i in indices_features]
                            x = x[x_selected]

                        k_fold = KFold(n_splits=10)
                        all_folds = k_fold.split(x)
                        all_absolute_error_from_cv = []
                        for train_index, test_index in all_folds:
                            x_train, x_test = x.iloc[train_index], x.iloc[test_index]
                            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                            reg.fit(x_train, y_train)  # changed from , y_train
                            prediction = reg.predict(x_test)
                            all_absolute_error_from_cv.append(mean_absolute_error(y_test, prediction))

                        mean_absolute_error_res = np.mean(all_absolute_error_from_cv)

                        writer.writerow({'Days': day,
                                         'Corr': corr_hyper_param,
                                         'K_best': select_k_hyper_param,
                                         'Reg': reg,
                                         'Features': [x_selected],
                                         'Mean absolute error': mean_absolute_error_res,
                                         })

            data_frame = datafs.copy(deep=True)


if __name__ == '__main__':
    start = str(datetime.now())
    print('Started features finding at: {}'.format(start))

    find_features_runner(raw_data_file_name="./data/merged_all_2019-4-1-2019-6-20.csv",
                         output_path_name='1_years_all_stations_submit_test',
                         output_file_name='regression_all_stations_dataset_1_years.csv')

    end = str(datetime.now())
    print("Ended features finding at: {}".format(end))
