
from pandas.io.json import json_normalize
from DataProcess import *
from LocationBasedDataProcess import *


if __name__ == '__main__':
    getStationRangeData(43, 2019, 9, 20, 2019, 10, 1)
    file_name = '2019-9-20-2019-10-1'
    technion_final_test_dataframe = createDataFrame(file_name='{}/_{}.json'.format(43, file_name))
    technion_final_test_dataframe.to_csv('./data/{}/dataset_{}.csv'.format(43, file_name))

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



