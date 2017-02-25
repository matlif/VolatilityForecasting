# This main file is a sketch of the overall program
#  if you dont have this installed then here's how to install the module:
#  conda install -c https://conda.binstar.org/bashtage arch

from read_in_files import read_in_files
from NumDaysWeeksMonths import NumDaysWeeksMonths
from Volatility import *
from linear_regression import *
import matplotlib.pyplot as plt
from PastAsPresent import *
from RetCalculator import *
from sklearn.metrics import mean_squared_error as mse
from garch_pq_model import garch_model as gm


filenames = 'AUDUSD.csv'
#  reads in the files and puts them into dataframes, returns a dataframe called df
df, df_single_day, df_single_month = read_in_files(filenames)
days_weeks_months, num_days_per_year = NumDaysWeeksMonths(df=df)
daily_vol_result = daily_vol_calc(df, df_single_day, num_days_per_year)
daily_ret = RetCalculator.daily_ret_df(df, df_single_day, num_days_per_year)

MSE_oneday = PastAsPresent.today_tomorrow(daily_vol_result)
plt.show()
one_day_results = LinRegression.lin_reg(daily_vol_result, 1)


three_day_results = LinRegression.lin_reg(daily_vol_result, 3)

five_day_results = LinRegression.lin_reg(daily_vol_result, 5)
plt.show()

daily_garch11_mse = gm.garch_pq_mse(daily_vol_result,np.array(daily_ret['Return_Daily']),1,1,1)


print("hi")



# DailyVolDF(df_single_day, num_days_per_year)


# predict tomorrows volatility based on today (same for weekly and monthly
# #     -this also looks like linear regression
#
# # perform linear regression (using past 1, 3, 5, vols)
# linear_regression()
#
# # perform ARCH
# arch_model()
#
# # perform GARCH(1,1)
# garch11_model()
#
# errorplots()
#

