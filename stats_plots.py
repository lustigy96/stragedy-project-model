import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np


def drow_correlation_matrix(df, fields):
    new_df=df[fields];
    corrMatrix = new_df.corr()
    print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True)
    plt.show()

def plot_hist_and_log_hist(df, field):
    n, bins, patches = plt.hist(df[field], bins=200, density=True, facecolor='g', alpha=0.75)
    plt.title(field+"-hist")
    plt.show()
    n, bins, patches = plt.hist(np.log(np.array(df[field])), bins=200, density=True, facecolor='g', alpha=0.75)
    plt.title("log"+field+"-hist")
    plt.show()
