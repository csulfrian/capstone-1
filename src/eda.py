import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_plot(df, labels, countries, filename):
    '''
    Creates a stacked line chart of the data per country

    Inputs:
        df - the dataframe to graph
        labels - tuple of the label values (x_axis, y_axis, title)
        countries - list of countries for the legend
        filename - filename to save the chart to

    Output:
        a pretty plot!
    '''
    df = df.drop(['Country Name', 'Country Code', 'Indicator Name',
                  'Indicator Code', 'Unnamed: 0'], axis=1)\
           .dropna(axis=1)

    years = list(df[::-1])

    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

    for i, _ in enumerate(countries):
        ax.plot(df.iloc[i], alpha=0.8, label=countries[i])
    ax.set_title(labels[1])
    ax.set_xlabel('Year')
    ax.set_ylabel(labels[0])
    ax.set_xticklabels(years, rotation=60)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/plot-{filename}.png')
    plt.close('all')

    return fig


def batch_plots(df, country_codes, indicators):
    '''
    Batch out our line charts

    Inputs:
        df - the dataframe to graph
        country_codes - list of countries for the legend
        indicators - list of indicators to filter by

    Output:
        Chartzzz, dog!
    '''
    labels = [('% GDP', 'Government expenditure as percentage of GDP'),
              ('% spent', 'Percent of education dollars spent on primary ed'),
              ('Students / Teacher', 'Students per teacher in primary ed'),
              ('Number', 'Number of teachers in primary ed'),
              ('%', 'Percentage of labor force with advanced education'),
              ('Dollars', 'GDP per capita (current USD)')]

    filenames = ['gdp-spend',
                 'expenditure-primary',
                 'student-teacher-ratio',
                 'num-teachers',
                 'percent-advanced',
                 'gdp-per-capita']

    for i, _ in enumerate(country_codes):
        target = df[df['Indicator Code'] == indicators[i]]
        create_plot(target, labels[i], country_codes, filenames[i])


if __name__ == '__main__':
    df = pd.read_csv('data/processed/EdStatsAggregated.csv')

    with open('data/countries.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
    country_codes = data[0]

    with open('data/indicators.csv') as g:
        reader = csv.reader(g)
        data_ = list(reader)
    indicators = data_[0]

    plt.rcParams.update({'font.size': 16})
    plt.style.use('bmh')
    
    batch_plots(df, country_codes, indicators)
