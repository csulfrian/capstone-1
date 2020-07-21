import pandas as pd

def drop_empty(df):
    '''
    First - drops all rows that are empty
    Next - auto generates a list of column names to remove
        1970 - 1977 - very little data
        2020 - 2100 - all empty

    Output:
        cols_to_drop - list of column names
    '''

    # Empty row removal
    df['sum'] = df.sum(axis=1)
    df_to_clean = df[df['sum'] != 0]

    # Empty column removal
    cols_to_drop = ['Unnamed: 69', '2016', '2017']
    for year in range(1970, 1978):
        cols_to_drop.append(str(year))
    for year in range(2020, 2101, 5):
        cols_to_drop.append(str(year))

    df_cleaned = df_to_clean.drop(columns=cols_to_drop)
    df_cleaned = df_cleaned.drop(columns='sum')

    df_cleaned.to_csv('data/processed/EdStatsClean.csv')
    
    return df_cleaned

def country_df(df, country_code, indicators):
    '''
    calculates the individual dataframes for each country we're interested in, as well as the indicators we want to examine

    input:
        df - the original dataframe
        country_code - the three digit country code to filter by
        indicators - a list of indicators that we're interested in filtering by

    output:
        a dataframe that contains our data to work on
    '''
    country = df[df['Country Code'] == country_code]
    country_w_codes = country[country['Indicator Code'].isin(indicators)]

    # Save a copy of each countries' featurized data
    country_w_codes.to_csv(f'data/processed/{country_code}_individual.csv')

    return country_w_codes

if __name__ == '__main__':
    
    df_to_clean = pd.read_csv('data/raw/EdStatsData.csv')
    clean_df = drop_empty(df_to_clean)

    # The country codes that we want to run the process on
    country_codes = ['USA', 'SWE', 'AUS', 'DEU', 'CHE', 'GBR']

    '''
    The codes of the indicators that we want to explore
    See the README.md file for explanations of the codes
    '''
    codes = ['SE.XPD.TOTL.GD.ZS', 'SE.XPD.PRIM.ZS', 'SE.PRM.ENRL.TC.ZS', 'SE.PRM.TCHR', 'SL.TLF.ADVN.ZS', 'NY.GDP.PCAP.CD']
    
    joined = pd.DataFrame(clean_df.iloc[0]).T

    for country in country_codes:
        country_dfs = country_df(clean_df, country, codes)
        joined = pd.concat([joined, country_dfs], axis=0)
    
    joined.drop(index=4)\
          .reset_index(drop=True)\
          .to_csv('data/processed/EdStatsAggregated.csv')
