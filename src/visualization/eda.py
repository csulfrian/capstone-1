import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 

def create_plot(x_data, y_data, x_label, y_label, x_ticks, title, filename):
    fig, ax = plt.subplots(figsize=(12,8), dpi=72)

    ax.plot(x_data, y_data, color='m', alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(x_ticks)
    plt.tight_layout()
    plt.savefig(f'images/{filename}')
    
    return fig

def create_corr_heatmap(df):
    return df.corr(method='pearson')

if __name__ == '__main__':
    df = pd.read_csv('data/processed/EdStatsAggregated.csv')
    
    plt.style.use('bmh')

    gdp_by_country = df[df['Indicator Code'] == 'SE.XPD.TOTL.GD.ZS']
    
    # Plot data for the US spending
    # y = .drop(['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 0'], axis=1).dropna(axis=1)
    # x = y.columns
    # y = y.values.flatten()
    # x_ticks = [str(x) for x in range(1986, 2015, 4)]
    # create_plot(x, y, x_label='Year', y_label='% GDP', x_ticks=x_ticks, title='Education Spending, USA', filename='us_spending.png')

