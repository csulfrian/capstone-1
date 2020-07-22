import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


plt.rcParams.update({'font.size': 16})
plt.style.use('bmh')

df = pd.read_csv('data/processed/EdStatsAggregated.csv')

country_codes = ['USA', 'SWE', 'AUS', 'DEU', 'CHE', 'GBR']


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

    fig, ax = plt.subplots(figsize=(12, 8), dpi=72)

    for i, _ in enumerate(countries):
        ax.plot(df.iloc[i], alpha=0.8, label=countries[i])
    ax.set_title(labels[2])
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_xticklabels(years, rotation=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/{filename}')
    plt.close('all')

    return fig


def create_corr_heatmap(df):
    return df.corr(method='pearson')


def gdp_by_country(df):
    return df[df['Indicator Code'] == 'SE.XPD.TOTL.GD.ZS']


def advanced_ed_by_country(df):
    return df[df['Indicator Code'] == 'SL.TLF.ADVN.ZS']


def num_teachers_by_country(df):
    return df[df['Indicator Code'] == 'SE.PRM.TCHR']


if __name__ == '__main__':
    # Spending on education by GDP plot
    gdps = gdp_by_country(df)
    labels = ('Year', '% GDP', 'Government expenditure on education as % of GDP')
    create_plot(gdps, labels, country_codes, filename='GDPs')

    # Percentage of labor force with advanced educations
    advanced_ed = advanced_ed_by_country(df)
    labels = ('Year', '%', 'Percent of labor force with advanced educations')
    create_plot(advanced_ed, labels, country_codes, filename='advanced-ed')

    # Number of teachers in primary ed
    num_teachers = num_teachers_by_country(df)
    labels = ('Year', 'Number', 'Number of teachers in primary education')
    create_plot(num_teachers, labels, country_codes, filename='num-teachers')

    # GDP per capita
    gdp_per_capita = df[df['Indicator Code'] == 'NY.GDP.PCAP.CD']
    labels = ('Year', 'Dollars', 'GDP per capita (current USD)')
    create_plot(gdp_per_capita, labels, country_codes, filename='gdp-per-capita')
