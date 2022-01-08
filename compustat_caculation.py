import pandas as pd
import const
import numpy as np
import get_data

import manage_df


def get_industry_data(d_path):
    df_all_industry = pd.read_csv(d_path, index_col=0)
    df_ind_by_sectors=manage_df.separate_to_df_arr_by_uniqe_field(df_all_industry,"gsector");
    df_ind_data=pd.DataFrame();
    arr_tot_sales_data, arr_gic_data,arr_year_data, arr_avg_assets_data=[], [], [],[]
    arr_ind_concentration = []
    for df_by_gic in df_ind_by_sectors:
        df_by_year=manage_df.separate_to_df_arr_by_uniqe_field(df_by_gic,"fyear");
        for df_by_gic_by_year in df_by_year:
            if(df_by_gic_by_year.empty): continue;
            ind_sales= np.sum(np.nan_to_num(np.array(df_by_gic_by_year.loc[:,'sale'])));
            ind_concentrations = np.sum(np.power(np.nan_to_num(np.array(df_by_gic_by_year.loc[:,'sale']))/ind_sales,2))
            ind_avg_tot_assets = np.average(np.nan_to_num(np.array(df_by_gic_by_year.loc[:,'at'])))
            arr_tot_sales_data.append(ind_sales)

            arr_gic_data.append(np.array(df_by_gic_by_year.loc[:,'gsector'])[0])
            arr_year_data.append(np.array(df_by_gic_by_year.loc[:,'fyear'])[0])
            arr_avg_assets_data.append(ind_avg_tot_assets)
            arr_ind_concentration.append(ind_concentrations)

    df_ind_data["gsector"]=arr_gic_data
    df_ind_data["fyear"]=arr_year_data
    df_ind_data["ind_avg_assets"]=arr_avg_assets_data
    df_ind_data["ind_tot_sales"]=arr_tot_sales_data
    df_ind_data["ind_concentration"] = arr_ind_concentration

    return df_ind_data

'''
    example:
    df = compustat_caculation.compustat_normal_data(constants.d_loc+constants.d_compustat_path_postfix+"snp-500-compustat-2.csv")
    df.to_csv(constants.d_loc+constants.d_compustat_path_postfix+"snp-500-compustat-2-nomalized.csv",index=False)
'''
#create df with the relevant values, out of compustat original parameters
def compustat_normal_data(d_path,df_industry):
    df_src = pd.read_csv(d_path, index_col=0)
    add_from_industry = ['ind_avg_assets','ind_tot_sales','ind_concentration']
    df_src = manage_df.add_col_from_df_by_uniqe_fileds(df_src,
                                              df_industry,
                                              'gsector',
                                              'fyear',
                                              add_from_industry,
                                                const.compustat_ctrl_tot_data,
                                                True)
    df_normalized = pd.DataFrame();

    xsga = np.nan_to_num(np.array(df_src.loc[:, 'xsga']))
    xrd = np.nan_to_num(np.array(df_src.loc[:, 'xrd']))
    sale = np.nan_to_num(np.array(df_src.loc[:, 'sale']))
    at = np.nan_to_num(np.array(df_src.loc[:, 'at']))
    prcc_c = np.nan_to_num(np.array(df_src.loc[:, 'prcc_c']))
    prcc_f = np.nan_to_num(np.array(df_src.loc[:, 'prcc_f']))
    csho = np.nan_to_num(np.array(df_src.loc[:, 'csho']))
    # ni = np.nan_to_num(np.array(df_src.loc[:, 'ni']))
    mkvalt = np.nan_to_num(np.array(df_src.loc[:, 'mkvalt']))
    bkvlps = np.nan_to_num(np.array(df_src.loc[:, 'bkvlps']))
    ceq = np.nan_to_num(np.array(df_src.loc[:, 'ceq']))
    ind_tot_sales = np.nan_to_num(np.array(df_src.loc[:, 'ind_tot_sales']))

    calculations_map = {
       "ticker_name": np.nan_to_num(np.array(df_src.loc[:, 'tic'])),
        "year": np.nan_to_num(np.array(df_src.loc[:, 'fyear'])),
        "sic": np.nan_to_num(np.array(df_src.loc[:, 'sic'])),
        "gsector":np.nan_to_num(np.array(df_src.loc[:, 'gsector'])),
        "book_value": np.nan_to_num(np.array(df_src.loc[:, 'bkvlps'])),
        "capx": np.nan_to_num(np.array(df_src.loc[:, 'capx'])),
        "at" : np.nan_to_num(np.array(df_src.loc[:, 'at'])),
       "ind_avg_assets": np.nan_to_num(np.array(df_src.loc[:, 'ind_avg_assets'])),
       "ind_tot_sales": np.nan_to_num(np.array(df_src.loc[:, 'ind_tot_sales'])),
       "ind_concentration": np.nan_to_num(np.array(df_src.loc[:, 'ind_concentration'])),
       "sale": sale,
        "firm_size": np.log(at),
        "tubins_q": (at + (csho * prcc_f) - ceq) / at,
        "market_to_book_ratio": bkvlps / mkvalt,
        "market_share_val": sale/ind_tot_sales,
        "market_value": mkvalt,
       "marketing_intensity": (xsga -xrd) / sale,
       "RD_intensity": xrd / at,
       # "book_value_on_equity": prcc_c * csho,
       # "earning_per_share": ni / csho,
       # "roe": ni/(csho*prcc_f),
    }
    for calc_parameter in calculations_map.keys():
        df_normalized[calc_parameter] = calculations_map[calc_parameter]
    return df_normalized