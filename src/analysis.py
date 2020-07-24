import csv
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


def make_dfs(codes):
    file_list = []
    for i, code in enumerate(codes):
        i = pd.read_csv(f'data/processed/{code}.csv')
        file_list.append(i)

    return file_list


def calculate_pdf_params(df, country):
    df = df[df['Country Code'] == country].dropna(axis=1)
    df = df.drop(['Unnamed: 0',
                  'Country Name',
                  'Country Code',
                  'Indicator Name',
                  'Indicator Code'], axis=1)

    mean, std = df.iloc[0].mean(), df.iloc[0].std()
    min_, max_ = df.iloc[0].min(), df.iloc[0].max()

    normal = stats.norm(mean, std)
    x = np.linspace(mean - (std * 3), mean + (std * 3), 1000)

    return normal, x


def plot_pdf(df, labels, country_codes, filename, execute=True):
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
    fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=300)

    for code in country_codes:
        normal, x = calculate_pdf_params(df, code)
        ax.plot(x, normal.pdf(x), label=code)
    ax.set_title(labels[1])
    ax.set_xlabel(labels[0])
    ax.set_ylabel('PDF')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/pdf-{filename}.png')
    plt.close('all')

    return fig


def batch_pdfs(country_codes, indicators):
    '''
    Batches all the pdf chart saving

    Input:
        indicators - the indicators we want to use
    '''
    dfs = make_dfs(indicators)

    labels = [('Percent', 'Government expenditure as percentage of GDP'),
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

    for i, data in enumerate(dfs):
        plot_pdf(data, labels[i], country_codes, filenames[i])


def create_heatmap(df, country, filename, method='spearman'):
    '''
    Create a correlation heatmap.

    Inputs:
        df - the DataFrame to run the test on
        method - the correlation method to be used, default Pearson

    Output:
        A saved heatmap for each country
    '''
    df = df.drop(['Country Name',
                  'Country Code',
                  'Indicator Name',
                  'Unnamed: 0'], axis=1)\
           .set_index('Indicator Code')\
           .T.dropna(axis=0)

    correlation_matrix = df.corr(method)

    mask = np.triu(np.ones_like(correlation_matrix.corr(), dtype=np.bool))

    readable_labels = ['% spent on primary',
                       'GDP per capita',
                       '% of GDP on Edu',
                       '% workers advanced ed',
                       'Student/teacher ratio',
                       'Num teachers in primary']

    plt.figure(figsize=(12, 8))

    heat = sns.heatmap(correlation_matrix, mask=mask,
                       vmin=-1, vmax=1, cmap='BrBG')
    heat.set_yticklabels(readable_labels)
    heat.set_xticklabels(readable_labels, rotation=45)
    heat.set_title(f'{method.title()} Correlation Heatmap - {country}',
                   fontdict={'fontsize': 18}, pad=12)
    plt.savefig(f'images/heatmap-{filename}.png',
                dpi=300, bbox_inches='tight')
    plt.close('all')

    return correlation_matrix


def batch_heatmaps():
    '''
    Batches the heatmap generation and saving
    '''
    filepath = 'data/processed/'

    countries_filenames = {'United States': 'USA',
                           'Sweden': 'SWE',
                           'Brazil': 'BRA',
                           'Germany': 'DEU',
                           'Switzerland': 'CHE',
                           'Costa Rica': 'CRI'}

    for country, filename in countries_filenames.items():
        create_heatmap(pd.read_csv(f'{filepath}/{filename}_individual.csv'),
                       country, filename)


if __name__ == '__main__':
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

    batch_pdfs(country_codes, indicators)

    batch_heatmaps()
