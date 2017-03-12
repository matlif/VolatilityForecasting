import numpy as np
import pandas as pd
from Performance_Measure import *
from SEplot import se_plot as SE


def KNN(vol_data, k=1, warmup=400, filename=None, Timedt=None):
    vol_data_input = vol_data['Volatility_Time']
    dates = vol_data['Date']
    return KNNcalc(vol_data=vol_data_input, dates =dates, k=k, warmup=warmup,filename=filename, Timedt=Timedt)


def KNNcalc(vol_data, dates=None, k=1, warmup=400, filename=None, Timedt=None):
    """
    # we now want to predict the volatility at time, t_warmup,
    # so we subtract vol @t_warmup from every point in train set
    # now we sort the abs value of these differences in ascending order (but without necessarily applying abs)
    # the first index is just the last_sample, so we will ignore it and choose the first 1-k samples' indices
    # recall in python indexing that the last index is not included, so for k = 1, only index 1 is chosen,
    # we add 1 to get the indices for the predicted vol

    # we now attempt to find the value of c. Below is ||sigma_t - sigma_k's||^2

    So how do we solve for c?
    Well we know that alpha_j = c / ||sigma_t - sigma_k's||

    and sum(alpha_j for all j's) = 1 = alpha_1 + alpha_2 + ... + alpha_k
    then:
    1 = c / ||sigma_t - sigma_1nn|| + c / ||sigma_t - sigma_2nn|| + ... c / ||sigma_t - sigma_knn||

    factoring out c:

    1 = c ( 1/||sigma_t - sigma_1nn|| + 1 / ||sigma_t - sigma_2nn|| + ... 1 / ||sigma_t - sigma_knn|| )

    So c = 1 / ( 1/||sigma_t - sigma_1nn|| + 1 / ||sigma_t - sigma_2nn|| + ... 1 / ||sigma_t - sigma_knn|| )

    # the sigmass are for the time point ahead of the nearest neighbor...these will be used for the prediction

    :param vol_data: pd.Series or pd.DataFrame object. If DF, then call a particular column using df.column_name
    :param k: nearest neighbors. Should be type(int)
    :param warmup: initial training period. Should be type(int)
    :param filename: None, for default case
    :return:
    """

    if filename is None:
        filename = " "
    # initialize
    prediction = pd.Series()
    iterator = 0
    try:
        while iterator < (len(vol_data)-warmup):
            # load in the datapoints
            # moving window
            train_set = vol_data[iterator:(warmup+iterator)]

            last_sample = train_set.iloc[- 1]
            diff = last_sample - train_set
            absdiff = diff.abs().sort_values()
            kn_index = diff.reindex(absdiff.index)[1:k + 1].index + 1

            squared = absdiff[1:k + 1] ** 2

            c = 1 / sum(1/squared)
            alpha_j = c/squared
            sigma = vol_data[kn_index]
            prediction = prediction.append(pd.Series([np.dot(alpha_j, sigma)], index=[iterator]))
            iterator += 1
            # print(prediction)
        # print(prediction)
    except:
        TypeError('Not a pd.Series or pd.DataFrame')
        ValueError("bad values")

    # now calculate MSE, QL and so forth
    Performance_ = PerformanceMeasure()
    MSE = Performance_.mean_se(observed=vol_data.iloc[warmup:], prediction=prediction)
    QL = Performance_.quasi_likelihood(observed=vol_data.iloc[warmup:], prediction=prediction)

    label = str(filename) + " " + str(Timedt) + " SE (" + str(k) + ") KNN Volatility"
    print(label)
    """ return a plot of the Squared error"""
    SE(vol_data.iloc[warmup:], prediction, dates.iloc[warmup:], function_method=label)

    return MSE, QL

# sanity check:  len(train_set) + len(prediction) == len(vol_data)