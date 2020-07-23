import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

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
    x = np.linspace(mean - (std * 3), mean + (std * 3), 1000)

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


def create_corr_heatmap(df):
    to_correlate = pd.read_csv('data/processed/DEU_individual.csv')
    to_correlate = to_correlate.drop(['Country Name', 'Country Code', 'Indicator Name', 'Unnamed: 0'], axis=1).set_index('Indicator Code').T.dropna(axis=0)

    correlation = to_correlate.corr(method='pearson')


    corr_target = abs(correlation['NY.GDP.PCAP.CD'])
    relevant_codes = corr_target[corr_target > 0.75]

    mask = np.triu(np.ones_like(correlation.corr(), dtype=np.bool))

    plt.figure(figsize=(16, 8))

    heatmap = sns.heatmap(correlation, mask=mask, vmin=-1, vmax=1, cmap='BrBG')
    heatmap.set_xticklabels(correlation.columns, rotation=45)
    heatmap.set_title('Pearson Correlation Heatmap - Germany', fontdict={'fontsize':18}, pad=12)
    plt.savefig('images/DEU-pearson-heatmap.png', dpi=300, bbox_inches='tight')
    plt.close('all')

    return fig


if __name__ == '__main__':
    exp_gdp, exp_pri, t_s_ratio, num_teachers, pct_adv, gdp_person = make_dfs(codes)
    all_dfs = make_dfs(codes)
    
    # Percentage advanced education
    # labels = ('%', 'Percentage of labor force with advanced education')
    # plot_pdf(pct_adv, labels, country_codes, filename='percent-advanced')
    
    # # Percentage spent or primary ed
    # labels = ('% spent', 'Percentage of education dollars spent on primary ed')
    # plot_pdf(exp_pri, labels, country_codes, filename='expenditure-primary')

    # # Teacher / student ratio
    # labels = ('Students / Teacher', 'Ratio of students to teachers in primary ed')
    # plot_pdf(t_s_ratio, labels, country_codes, filename='student-teacher-ratio')

    # # GDP per capita
    # labels = ('Dollars', 'GDP per capita (current USD)')
    # plot_pdf(gdp_person, labels, country_codes, filename='gdp-per-capita')

    # # GDP % on education
    # labels = ('Percent', 'Government expenditure as percentage of GDP')
    # plot_pdf(exp_gdp, labels, country_codes, filename='gdp-spend')

    # Number of teachers in primary ed
    # !!!! OI! POPULATIONS VARY WIDELY! ADJUSTMENT FACTOR NEEDED !!!!
    # labels = ('Number', 'Number of teachers in primary ed')
    # plot_pdf(num_teachers, labels, country_codes, filename='num-teachers')
    to_correlate = pd.read_csv('data/processed/DEU_individual.csv')
    to_correlate = to_correlate.drop(['Country Name', 'Country Code', 'Indicator Name', 'Unnamed: 0'], axis=1).set_index('Indicator Code').T.dropna(axis=0)



    # each = to_correlate.iloc[0].mean()

    one = to_correlate['NY.GDP.PCAP.CD'].dropna()
    two = to_correlate['SL.TLF.ADVN.ZS'].dropna()

    stat, p_val = stats.ttest_ind(one, two, equal_var=False)

    def std_err(sample):
        return sample.std() / (len(sample)**0.5)
    normal = stats.norm(loc=one.mean(), scale=one.std())
    z = (two.mean() - one.mean()) / std_err(one)
    p = 1 - normal.cdf(two.mean())

    fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=300)
    x = np.linspace(0, 100, 10)
    ax.plot(x, normal.cdf(x))