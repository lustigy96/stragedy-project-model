import const
import re
from manage_df import *

location_path =  const.d_loc + const.d_proccessed_path_postfix

def calc_age():
        df_sp500 = pd.read_csv(const.sp500_info_file)
        age_ticker = {}
        symbols = np.array(df_sp500.loc[:, 'ticker_name'])
        founds = np.array(df_sp500.loc[:, 'Founded'])
        for symbol, found in zip(symbols, founds):
                years = re.findall("\d*", found)
                age_ticker[symbol] = 2022 - int(years[0])
        # print(age_ticker)
        return age_ticker

def add_col_from_df_to_dic(df_add_to, keys, uniqe_id1, uniqe_id2, new_col_name_list,dest_file):
    src_uniqe_rows_arr = df_add_to[[uniqe_id1]].values
    for new_col_name in new_col_name_list:
        coll2add = []
        for row_ids in src_uniqe_rows_arr:
            val_row = keys[row_ids[0]]
            coll2add.append(val_row)
        df_add_to[new_col_name] = coll2add
    df_add_to.to_csv(dest_file, index=False)
    return df_add_to

def add_age_to_csv(path,  dic_age):
        df = pd.read_csv(path )
        # symbols = np.array(df.loc[:, 'ticker_name'])
        # names = [_ for _ in 'Age']
        # df = pd.DataFrame(df, index=names, columns=names)
        # df.to_csv('df.csv', index=True, header=True, sep=' ')
        list2add = ['Age']
        add_col_from_df_to_dic(df, dic_age,
                                        'ticker_name',
                                        "Age",
                                        list2add,
                                        os.path.splitext(path)[0] + "_age.csv")
        # for symbol in zip(symbols):
        #         np.append


if __name__ == '__main__':
        age_ticker = calc_age()
        add_age_to_csv(location_path + const.compustat_ctrl_tot_fname, age_ticker)
        add_age_to_csv(location_path + const.compustat_filter_ctrl, age_ticker)
        add_age_to_csv(location_path + "marketing_intensity_relevants.csv", age_ticker)
        add_age_to_csv(location_path + "rd_intensity_relevants.csv", age_ticker)
        add_age_to_csv(location_path + "rd_mki_intensity_relevants.csv", age_ticker)