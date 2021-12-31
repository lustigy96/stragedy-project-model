# from sklearn.linear_model import LinearRegression
# import statsmodels.api as sm
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import const
import manage_df

def get_linear_reg_1_var(x_name,y_name,df, paint=False):
    samples=min(500,len(df[x_name]))
    x = list(df[x_name]) [0:samples]
    y = list(df[y_name]) [0:samples]
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    if(paint):
        myfunc = slope * np.array(x) + intercept
        plt.scatter(x, y)
        plt.plot(x, myfunc)
        plt.show()
    return slope, intercept, r, p, std_err

def resression_1var_to_df(y_fields_list,x_fild,df):
    slope_arr, intercept_arr, r_arr, p_arr, std_err_arr, is_distinct_arr = [],[],[],[],[],[]
    data=[slope_arr, intercept_arr, r_arr, p_arr, std_err_arr, is_distinct_arr]
    for y_field in y_fields_list:
        res=list(get_linear_reg_1_var(x_fild,y_field,df,True))
        for arr, r in zip(data[:-1],res):
            arr.append(r)
        is_distinct_arr.append(res[3]<const.p_distinction_val)

    data_to_df=[y_fields_list,x_fild]
    data_to_df.extend(data)
    col_names=['y','x','slope','intercept','r','p','std_err','is_distinct_arr']
    return manage_df.data_to_df(col_names, data_to_df)
