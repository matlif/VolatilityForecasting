from SEplot import se_plot as SE
import pandas as pd
from arch import arch_model
from Performance_Measure import *

class ArchModelQ(object):
    """
            arch(q) model generalized for daily, weekly and monthly data

    :return: weekly_ret
    """
    def __init__(self, df):
        self.df = df

    def arch_q(ret, q, lags):

        # from arch import arch_model
        # The default set of options produces a model with a constant mean, GARCH(1,1) conditional variance\
        #  and normal errors.
        archq = arch_model(ret, q=q, lags=lags, vol="Arch")
        res = archq.fit(update_freq=1, disp='off', show_warning=False)
        forecasts = res.forecast()

        return forecasts.variance['h.1'][1]

    def arch_q_mse(data, ret, q, lags):

        # from sklearn.metrics import mean_squared_error as mse
        import matplotlib.pyplot as plt

        arch_q_forecasts = []
        for i in range(len(ret)-2):
            arch_q_forecasts.append(ArchModelQ.arch_q(ret[i:(i+lags+1)], q, lags))
        # observed daily vol
        observed = data['Volatility_Daily'][2:]
        arch_q_forecasts = pd.Series(arch_q_forecasts)

        # Instantiate the class and pass the mean_se and quasi_likelihood functions
        Performance_ = PerformanceMeasure()
        MSE = Performance_.mean_se(observed=observed, prediction=arch_q_forecasts)
        QL = Performance_.quasi_likelihood(observed=observed, prediction=arch_q_forecasts)

        # output = mse(observed, arch_q_forecasts)

        SE(observed, arch_q_forecasts)
        plt.title(str(lags) + " Day Lag's SE: ARCH(" + str(q) + ") ")

        # plt.show()
        return MSE, QL




        # def garch_pq(ret, p, q,lags):
    #
    #     from arch import arch_model
    #     # The default set of options produces a model with a constant mean, GARCH(1,1) conditional variance\
        #  and normal errors.
    #     garchpq = arch_model(ret[1:3],p=p, q=q,lags=lags)
    #     res = garchpq.fit(update_freq=1)
    #     forecasts = res.forecast()
    #     print(forecasts.variance)
    #     # print(res.summary())


    # from arch import arch_model
    # garch11 = arch_model(r, p=1, q=1)
    # res = garch11.fit(update_freq=10)
    # print(res.summary())
