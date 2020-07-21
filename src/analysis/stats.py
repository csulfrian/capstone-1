import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

country_codes = ['USA', 'SWE', 'AUS', 'DEU', 'CHE', 'GBR']
codes = ['SE.XPD.TOTL.GD.ZS',
            'SE.XPD.PRIM.ZS',
            'SE.PRM.ENRL.TC.ZS',
            'SE.PRM.TCHR',
            'SL.TLF.ADVN.ZS',
            'NY.GDP.PCAP.CD']

def make_dfs(codes):
    file_list = []
    for i, code in enumerate(codes):
        i = pd.read_csv(f'data/processed/{code}.csv')
        file_list.append(i)

    return file_list

def get_normal_dist(df):
    return stats.norm(df.iloc[0].mean(), df.iloc[0].std())


if __name__ == '__main__':
    files = make_dfs(codes)
    
    # normal = get_normal_dist(df)

    # fig, ax = plt.subplots(figsize=(12, 8))
    # x = np.linspace(4, 6, num=100)
    # ax.plot(x, normal.pdf(x))
    # ax.plot(normal.cdf(x))
    # plt.show()