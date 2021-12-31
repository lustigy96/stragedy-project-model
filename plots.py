import matplotlib.pyplot as plt
import numpy as np

def multiple_g_on_same_axis(df_array, x_col_name, y_col_name, ax):
    for df in df_array:
        x=np.array(df.loc[:, x_col_name])
        y = np.array(df.loc[:, y_col_name])
        if( np.all((x == 0)) or np.all((y == 0))): continue
        ax.plot(x, y,'go')
    ax.set_title(y_col_name+" as a function of " +x_col_name)

def subplot(plot_function, args_3,x,y):
    figure, axis = plt.subplots(x, y)
    for x_idx in range(x):
        for y_idx in range(y):
            plot_function(args_3[x_idx+y_idx*y][0], args_3[x_idx+y_idx*y][1], args_3[x_idx+y_idx*y][2], axis[y_idx, x_idx])
    return figure, axis
