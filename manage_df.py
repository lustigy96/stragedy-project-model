import pandas as pd
import os
import numpy as np

# returns list of df, out of all files in a directory, with the relevant fields
# if tickers_list is empty, do to all files in directory
def data2df(d_location, fields_list=[], tickers_list=[]):
    if(len(tickers_list)==0):  tickers_list = os.listdir(d_location).sort()
    if(len(fields_list)) > 0:
        df_list = [pd.read_excel(d_location+ticker_name, index_col=0).filer(itmes=fields_list) for ticker_name in tickers_list]
    else:
        df_list = [pd.read_excel(d_location+ticker_name, index_col=0) for ticker_name in tickers_list]
    return df_list;

def concat_df(df_list, f_horizonal=0):
    return pd.concat(df_list, axis=f_horizonal)

#separate to multiple df, one for each ticker
def separate_to_df_arr_by_uniqe_field(df_all,separate_uniqe_col_name):
    all_tickers= df_all[separate_uniqe_col_name].unique()
    separed_df_array = [df_all[df_all[separate_uniqe_col_name] ==tick] for tick in all_tickers]
    return separed_df_array;

# ignore irrelevant tickers, with 0 in rd or in marketing
def filter_df_with_zeros_fields(df_array, list_of_fields):
    df_arr_filtered=[]
    for df in df_array:
        add=True
        for field in list_of_fields:
            field_col_arr = np.nan_to_num(df[field])
            if(np.all(np.array(field_col_arr)==0)):
                add=False
        if(add): df_arr_filtered.append(df)
    return df_arr_filtered

def filter_row_with_inf_0_nan(df_src, list_of_fields=[], filter_inf= True, fileter_zero=True):
    df = df_src.copy()
    values_to_filter_by=[]
    if (filter_inf): values_to_filter_by.extend([np.inf, - np.inf])
    if (fileter_zero): values_to_filter_by.extend([0])
    if(len(list_of_fields)==0): list_of_fields= df.columns
    df[list_of_fields].replace(values_to_filter_by, np.nan, inplace = True)
    df = df.dropna()
    return df

def add_col_from_df(df_source,df_dest,col_name_to_add, col_common_id):
    df_to_merge=df_source[[col_common_id, col_name_to_add]]
    return df_dest.merge(df_to_merge, how='left')

def data_to_df(col_names,data_arrays):
    df = pd.DataFrame(columns=col_names)
    for col, data in zip(col_names,data_arrays):
        df[col]=data
    return df
