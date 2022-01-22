import pandas as pd
import const
import numpy as np
import manage_df


def get_industry_data(d_path):
    df_all_industry = pd.read_csv(d_path, index_col=0)
    df_all_industry["sic_2"] = np.floor(np.nan_to_num(np.array(df_all_industry.loc[:, 'sic'])) / 100)
    df_ind_by_sectors=manage_df.separate_to_df_arr_by_uniqe_field(df_all_industry,"sic_2");
    df_ind_data=pd.DataFrame();
    arr_tot_sales_data, arr_sic2_data,arr_year_data, arr_avg_assets_data=[], [], [],[]
    arr_ind_concentration = []
    for df_by_sic_2 in df_ind_by_sectors:
        df_by_year=manage_df.separate_to_df_arr_by_uniqe_field(df_by_sic_2,"fyear");
        for df_by_sic_2_by_year in df_by_year:
            if(df_by_sic_2_by_year.empty): continue;
            ind_sales= np.sum(np.nan_to_num(np.array(df_by_sic_2_by_year.loc[:,'sale'])));
            ind_concentrations = np.sum(np.power(np.nan_to_num(np.array(df_by_sic_2_by_year.loc[:,'sale']))/ind_sales,2))
            ind_avg_tot_assets = np.average(np.nan_to_num(np.array(df_by_sic_2_by_year.loc[:,'at'])))
            arr_tot_sales_data.append(ind_sales)

            arr_sic2_data.append(np.array(df_by_sic_2_by_year.loc[:,'sic_2'])[0])
            arr_year_data.append(np.array(df_by_sic_2_by_year.loc[:,'fyear'])[0])
            arr_avg_assets_data.append(ind_avg_tot_assets)
            arr_ind_concentration.append(ind_concentrations)

    df_ind_data["sic_2"]=arr_sic2_data
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
    df_src = pd.read_csv(d_path, index_col=1)
    df_src["sic_2"] = np.floor(np.nan_to_num(np.array(df_src.loc[:, 'sic'])) / 100)
    add_from_industry = ['ind_avg_assets','ind_tot_sales','ind_concentration']
    df_src = manage_df.add_col_from_df_by_uniqe_fileds(df_src,
                                              df_industry,
                                              'sic_2',
                                              'fyear',
                                              add_from_industry,
                                                const.compustat_ctrl_tot_data,
                                                True)
    df_normalized = pd.DataFrame();
    xsga = np.nan_to_num(np.array(df_src.loc[:, 'xsga']))
    capx= np.nan_to_num(np.array(df_src.loc[:, 'capx']))
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
    sic= np.nan_to_num(np.array(df_src.loc[:, 'sic']))
    rd_intensity= xrd / at
    mki = (xsga -xrd) / sale
    calculations_map = {
       "ticker_name": np.nan_to_num(np.array(df_src.loc[:, 'tic'])),
        "year": np.nan_to_num(np.array(df_src.loc[:, 'fyear'])),
        "gvkey": np.nan_to_num(np.array(df_src.loc[:, 'gvkey'])),
        "sic": sic,
        "sic_2": np.floor(sic/100),
        "gsector":np.nan_to_num(np.array(df_src.loc[:, 'gsector'])),
        "book_value": np.nan_to_num(np.array(df_src.loc[:, 'bkvlps'])),
        "capx_scaled": capx/sale,
        "at" : np.nan_to_num(np.array(df_src.loc[:, 'at'])),
       "ind_avg_assets": np.nan_to_num(np.array(df_src.loc[:, 'ind_avg_assets'])),
       "ind_tot_sales": np.nan_to_num(np.array(df_src.loc[:, 'ind_tot_sales'])),
       "ind_concentration": np.nan_to_num(np.array(df_src.loc[:, 'ind_concentration'])),
       "sale": sale,
        "firm_size": np.log(at),
        "tobins_q": (at + (csho * prcc_f) - ceq) / at,
        "log-tobins_q": np.log((at + (csho * prcc_f) - ceq) / at),
        "market_to_book_ratio": bkvlps / mkvalt,
        "market_share_val": sale/ind_tot_sales,
        "market_value": mkvalt,
       "marketing_intensity": mki,
        "marketing_intensity_squered": np.power(mki, 2),
       "RD_intensity": rd_intensity,
        "RD_intensity_squered": np.power(rd_intensity,2),
        "RD_intensity_mki": rd_intensity *mki,
        "RD_intensity_squered_mki": np.power(rd_intensity, 2) * mki,
        "RD_intensity_mki_squered": rd_intensity * np.power(mki, 2),
       # "book_value_on_equity": prcc_c * csho,
       # "earning_per_share": ni / csho,
       # "roe": ni/(csho*prcc_f),
    }
    for calc_parameter in calculations_map.keys():
        df_normalized[calc_parameter] = calculations_map[calc_parameter]
    return df_normalized