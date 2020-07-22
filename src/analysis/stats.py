import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})
plt.style.use('bmh')

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


def calculate_pdf_params(df, country):
    df = df[df['Country Code'] == country].dropna(axis=1)
    df = df.drop(['Unnamed: 0', 'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], axis=1)

    mean, std = df.iloc[0].mean(), df.iloc[0].std()
    min_, max_ = df.iloc[0].min(), df.iloc[0].max()

    normal = stats.norm(mean, std)
    x = np.linspace(min_ - (std * 2), max_ + (std * 2), 1000)

    return normal, x


def plot_pdf(df, labels, country_codes, filename):
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
    fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=72)

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


if __name__ == '__main__':
    exp_gdp, exp_pri, t_s_ratio, num_teachers, pct_adv, gdp_person = make_dfs(codes)

    # Percentage advanced education
    labels = ('%', 'Percentage of labor force with advanced education')
    plot_pdf(pct_adv, labels, country_codes, filename='percent-advanced')
    
    # Percentage spent or primary ed
    labels = ('% spent', 'Percentage of education dollars spent on primary ed')
    plot_pdf(exp_pri, labels, country_codes, filename='expenditure-primary')

    # Teacher / student ratio
    labels = ('Students / Teacher', 'Ratio of students to teachers in primary ed')
    plot_pdf(t_s_ratio, labels, country_codes, filename='student-teacher-ratio')

    # GDP per capita
    labels = ('Dollars', 'GDP per capita (current USD)')
    plot_pdf(gdp_person, labels, country_codes, filename='gdp-per-person')

    # Number of teachers in primary ed
    # !!!! OI! POPULATIONS VARY WIDELY! ADJUSTMENT FACTOR NEEDED !!!!
    # labels = ('Number', 'Number of teachers in primary ed')
    # plot_pdf(num_teachers, labels, country_codes, filename='num-teachers')