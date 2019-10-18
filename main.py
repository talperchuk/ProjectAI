
from pandas.io.json import json_normalize
from DataProcess import *
from LocationBasedDataProcess import *


if __name__ == '__main__':
    # # Get the channels Ids based on one example # #
    #features = getChannelIds()
    
    # # Create data frame from a json file. # #
    datafs = createDataFrame(file_name='yotvata_july_2019-7.json')


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

    # Predict addons of multiple days and for changing corr hyper param (4/9/19)
    for day_addon in range(29):
    # try to classify.
        print('DAY: {}!!!!!!!!'.format(day_addon))
        addPreviousDaysFeatures(datafs, day_addon)
        print("**corr**")
        for col in datafs:
            mean = datafs[col].mean()
            datafs[col].fillna(mean, inplace=True)

        for corr_hyper in np.arange(0.1, 1, 0.1):
            print('################################# {} ##########################'.format(corr_hyper))
            corr, pred = getCorrelationOfDataForFeature(datafs, 'TD')
            new_dataframe = datafs[['TD'] + pred]
            model, x, y = getModelBackElimination(new_dataframe, pred, 'TD')
            ('********Final summary: {}'.format(model.summary()))
            predict(x, y)

