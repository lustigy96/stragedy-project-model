import pandas as pd
import manage_df
import compustat_caculation


def match_values_by_id(df_src, df_new_data, dest_path, value_col= "GICS Sector", common_id_col="ticker_name", first_time=False):
    if first_time:
        df_matched = manage_df.add_col_from_df(df_new_data, df_src, value_col, common_id_col)
        df_matched.to_csv(dest_path , index=False)
        return df_matched
    return pd.read_csv(dest_path)

def normalized_compustat(src_file, dest_file, df_industry, first_time=False):
    if first_time:
        df_all = compustat_caculation.compustat_normal_data(src_file, df_industry)

        df_all.to_csv(dest_file, index=False)
        return df_all
    return pd.read_csv(dest_file)

def get_industry_data(src_file, dest_file, first_time=False):
    if first_time:
        df_ind_summery = compustat_caculation.get_industry_data(src_file)
        df_ind_summery.to_csv(dest_file, index=False)
        return df_ind_summery
    return pd.read_csv(dest_file)

def get_filtered_rows_nan_inf_0(file_path, df=[], field_to_filter=[], first_time=False ):
    if first_time:
        filtered_df = manage_df.filter_row_with_inf_0_nan(df, field_to_filter)
        filtered_df.to_csv(file_path ,index=False)
        return filtered_df
    return pd.read_csv(file_path)


def get_only_relevant_tickers_df_arr(df_array, filer_zero_columns, file_path, first_time=False):
    if(first_time):
        filter_irrlevant = manage_df.filter_df_with_zeros_fields(df_array, filer_zero_columns)
        filter_irrlevant.to_csv(file_path, index=False)
        return filter_irrlevant
    return pd.read_csv(file_path, index_col=0)

def get_df(path):
    df = pd.read_csv(path)
    return df