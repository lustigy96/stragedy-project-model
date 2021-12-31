# This is a sample Python script.
import pandas as pd
import const
import plots
import manage_df
import get_data
import linear_regrations
import matplotlib.pyplot as plt

def plots_try(ticker_df_array):
    args= [[ticker_df_array, "RD_intensity", "market_value_change_precent"],
           [ticker_df_array, "RD_intensity", "roe"],
           [ticker_df_array, "RD_intensity", "marketing_intensity"],
           [ticker_df_array, "RD_intensity", "earning_per_share"]]
    figure, axis = plots.subplot(plots.multiple_g_on_same_axis, args, 2, 2)
    plt.show()

def create_compustat_data():
    df_compustat_normalized = get_data.normalized_compustat(const.compustat_original_data,
                                                            const.compustat_normalized_file, False)
    df_classification = pd.read_csv(const.sp500_info_file, index_col=0)
    df_compustat_normalized_classified = get_data.match_values_by_id(
        df_compustat_normalized,
        df_classification,
        const.compustat_normalized_calssified_file,
        value_col="GICS Sector",
        common_id_col="ticker_name",
        first_time=False)
    df_arr_by_company = manage_df.separate_to_df_arr_by_uniqe_field(df_compustat_normalized_classified, "ticker_name")
    df_relevant_mki = manage_df.concat_df(
        manage_df.filter_df_with_zeros_fields(df_arr_by_company, ["marketing_intensity"]))
    df_relevant_rdi = manage_df.concat_df(manage_df.filter_df_with_zeros_fields(df_arr_by_company, ["RD_intensity"]))
    df_mki_filter_rows = get_data.get_filtered_rows_nan_inf_0(
        file_path=const.compustat_mki,
        df=df_relevant_mki,
        field_to_filter=["marketing_intensity"],
        first_time=False)
    df_rdi_filter_rows = get_data.get_filtered_rows_nan_inf_0(
        file_path=const.compustat_rdi,
        df=df_relevant_rdi,
        field_to_filter=["RD_intensity"],
        first_time=False)
    return df_mki_filter_rows, df_rdi_filter_rows

def simple_linear_reg(df_rdi_filter_rows,df_mki_filter_rows):
    df_rdi_lin=linear_regrations.resression_1var_to_df(const.linear_regression_y,'RD_intensity',df_rdi_filter_rows)
    df_mki_lin=linear_regrations.resression_1var_to_df(const.linear_regression_y,'marketing_intensity',df_mki_filter_rows)

    all_simple_reg=manage_df.concat_df([df_rdi_lin,df_mki_lin])
    all_simple_reg.to_csv(const.Lregs_all_simple_file, index=False)

def simple_linear_reg_by_category(yvar_df_array, vary_name_arr):
    all_df = []
    for yvar_df, yvar_name in zip(yvar_df_array,vary_name_arr):
        df_arr_by_company = manage_df.separate_to_df_arr_by_uniqe_field(yvar_df, "GICS Sector")
        for sector_df in df_arr_by_company:
            linear_reg_df =linear_regrations.resression_1var_to_df(const.linear_regression_y, yvar_name, sector_df)
            r_reg_df , samples= linear_reg_df.shape[0], sector_df.shape[0] #returns number of rows in df
            linear_reg_df['samples'] = [samples] * r_reg_df
            linear_reg_df['sector']=[sector_df.iloc[0]['GICS Sector']] * r_reg_df
            if(samples < 100): continue
            all_df.append(linear_reg_df)
    manage_df.concat_df(all_df).to_csv(const.Lreg_all_simple_by_sector_file, index=False)

if __name__ == '__main__':
    df_rdi_filter_rows = get_data.get_filtered_rows_nan_inf_0(file_path=const.compustat_rdi)
    df_mki_filter_rows = get_data.get_filtered_rows_nan_inf_0(file_path=const.compustat_mki)
    simple_linear_reg(df_rdi_filter_rows, df_mki_filter_rows)
    #simple_linear_reg_by_category([df_rdi_filter_rows,df_mki_filter_rows],['RD_intensity','marketing_intensity'])

