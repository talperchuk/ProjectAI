import joblib
from DataProcess import *
from DataRetrival import *
from findFeaturesScript import *
from sklearn.metrics import mean_absolute_error

if __name__ == '__main__':
    print("***************Loading data...************************")
    reg = joblib.load('./data/Experiments/Model/TechnionBestResultReg.joblib')
    x_test = pd.read_csv('./data/Experiments/Model/TestSet.csv')
    x_test.set_index(x_test['Unnamed: 0'], inplace=True)
    x_test.index.name = ''
    x_test.drop(labels='Unnamed: 0', axis=1, inplace=True)
    print("***************Predicting...************************")
    prediction = reg.predict(x_test)
    y_test = pd.read_csv('./data/Experiments/Model/TestSetRealLabels.csv')
    y_test.set_index(y_test['Unnamed: 0'], inplace=True)
    y_test.index.name = ''
    y_test.drop(labels='Unnamed: 0', axis=1, inplace=True)
    print("***************Result************************")
    x = list(y_test['TD_tomorrow'])
    resList = zip(list(y_test.index), list(y_test['TD_tomorrow']), prediction)
    for res in resList:
        print("Date: {}\nReal Temp is: {:.5f}. Predicted Temp: {:.5f}".format(res[0], res[1], res[2][0]))
    print("\n")
    print("***************Mean Absolute Error Result************************")
    res = mean_absolute_error(y_test, prediction)
    print(res)
