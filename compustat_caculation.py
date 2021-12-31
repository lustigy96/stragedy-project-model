import pandas as pd
import const
import numpy as np

#create df with the relevant values, out of compustat original parameters
'''
    example:
    df = compustat_caculation.compustat_normal_data(constants.d_loc+constants.d_compustat_path_postfix+"snp-500-compustat-2.csv")
    df.to_csv(constants.d_loc+constants.d_compustat_path_postfix+"snp-500-compustat-2-nomalized.csv",index=False)
'''
def compustat_normal_data(d_path):
    df_src = pd.read_csv(d_path, index_col=0)
    df_normalized = pd.DataFrame();

    xsga = np.nan_to_num(np.array(df_src.loc[:, 'xsga']))
    xrd = np.nan_to_num(np.array(df_src.loc[:, 'xrd']))
    sale = np.nan_to_num(np.array(df_src.loc[:, 'sale']))
    at = np.nan_to_num(np.array(df_src.loc[:, 'at']))
    prcc_c = np.nan_to_num(np.array(df_src.loc[:, 'prcc_c']))
    prcc_f = np.nan_to_num(np.array(df_src.loc[:, 'prcc_f']))
    csho = np.nan_to_num(np.array(df_src.loc[:, 'csho']))
    ni = np.nan_to_num(np.array(df_src.loc[:, 'ni']))
    mkvalt = np.nan_to_num(np.array(df_src.loc[:, 'mkvalt']))
    bkvlps = np.nan_to_num(np.array(df_src.loc[:, 'bkvlps']))
    ceq = np.nan_to_num(np.array(df_src.loc[:, 'ceq']))

    calculations_map = {
       "ticker_name": np.nan_to_num(np.array(df_src.loc[:, 'tic'])),
       "marketing_intensity": (xsga -xrd) / sale,
       "RD_intensity": xrd / at,
       "book_value_on_equity": prcc_c * csho,
       "earning_per_share": ni / csho,
       "firm_size": np.log(at),
       "market_to_book_ratio":bkvlps / mkvalt,
       "market_value": mkvalt,
        "roe": ni/(csho*prcc_f),
        "tubins_q": (at+(csho*prcc_f)-ceq)/at,
        "year":  np.nan_to_num(np.array(df_src.loc[:, 'fyear'])),
        "book_value": np.nan_to_num(np.array(df_src.loc[:, 'bkvlps'])),
    }
    for calc_parameter in calculations_map.keys():
        df_normalized[calc_parameter] = calculations_map[calc_parameter]
    return df_normalized