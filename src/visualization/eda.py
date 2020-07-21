import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/processed/EdStatsAggregated.csv')

country_codes = ['USA', 'SWE', 'AUS', 'DEU', 'CHE', 'GBR']

plt.style.use('bmh')


def create_plot(df, ax, labels, countries, filename):
    '''
    Creates a stacked line chart of the data per country

    Inputs:
        df - the dataframe to graph
        ax - Matplotlib ax object
        labels - tuple of the label values (x_axis, y_axis, title)
        countries - list of countries for the legend
        filename - filename to save the chart to
    '''
    df = df.drop(['Country Name', 'Country Code', 'Indicator Name',
                  'Indicator Code', 'Unnamed: 0'], axis=1)\
           .dropna(axis=1)

    years = list(df[::-1])

    for i, _ in enumerate(countries):
        ax.plot(df.iloc[i], alpha=0.8, label=countries[i])
    ax.set_title(labels[2])
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_xticklabels(years, rotation=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/{filename}')
    plt.show()
    # plt.close()


def create_corr_heatmap(df):
    return df.corr(method='pearson')


def gdp_by_country(df):
    gdp_by_country = df[df['Indicator Code'] == 'SE.XPD.TOTL.GD.ZS']

    return gdp_by_country


if __name__ == '__main__':
    gdps = gdp_by_country(df)

    # Spending on education by GDP plot
    fig1, ax = plt.subplots(figsize=(12, 8), dpi=72)
    labels = ('Year', '% GDP', 'Government expenditure on education, % of GDP')
    create_plot(gdps, ax, labels, country_codes, filename='GDPs')
