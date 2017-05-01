import numpy as np
import pandas as pd


def KRR_append_and_csv(dictlist, filename, count, methodname, n , kernel, MSE, QL, lnSE, PredVol):
    """
    outputs from test set. this function made specifically for KRR but can be modified to BRR or others by removing 
    [kernel]
    
    :param dictlist: 
    :param methodname: 
    :param kernel: 
    :param MSE: 
    :param QL: 
    :param lnSE: 
    :param PredVol: 
    :return: 
    """
    dictlist[methodname][kernel]['krr1_mse_list'].append(MSE)
    dictlist[methodname][kernel]['krr1_ql_list'].append(QL)
    dictlist[methodname][kernel]['krr1_lnSE_list'].append(lnSE)
    dictlist[methodname][kernel]['krr1_PredVol_list'].append(PredVol)

    # print(str(name) + " BRR1(" + str(lr_optimal_n_list_benchmark[count]) + ")" + "log_lamdba_" + str(
    #     rr1_optimal_log_lambda) + " test MSE: " + str(MSE_RR1_test) + "; test QL: " + str(QL_RR1_test))



    krr1_lnse = dictlist[methodname][kernel]['krr1_lnSE_list'][count]
    krr1_predvol = dictlist[methodname][kernel]['krr1_PredVol_list'][count]

    krr1_lnSE_list_df = pd.DataFrame(np.array([krr1_lnse]), index=["krr1_lnSE"]).transpose()
    krr1_PredVol_list_df = pd.DataFrame(np.array([krr1_predvol]), index=["krr1_PredVol"]).transpose()

    # include the kernel when outputting to csv
    krr1_lnSE_list_df.to_csv(str(filename) + " " + str(kernel) + "kernel" + " krr1_lnSE.csv")
    krr1_PredVol_list_df.to_csv(str(filename) + " " + str(kernel) + "kernel" + " krr1_PredVol.csv")

    return dictlist
