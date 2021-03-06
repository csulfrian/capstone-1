import csv
import pandas as pd
import numpy as np


def drop_empty(df):
    '''
    First - drops all rows that are empty
    Next - auto generates a list of column names to remove
        1970 - 1977 - very little data
        2020 - 2100 - all empty

    Input:
        df - the DataFrame that needs to be cleaned

    Output:
        cols_to_drop - list of column names
    '''
    # Empty row removal
    df['sum'] = df.sum(axis=1)
    df_to_clean = df[df['sum'] != 0]

    # Empty/inconsistent column removal
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
    Calculates the individual dataframes for each country we're interested in,
    as well as the indicators we want to examine

    input:
        df - the original dataframe
        country_code - the three digit country code to filter by
        indicators - a list of indicators that we're interested in filtering by

    output:
        a dataframe that contains our data to work on
    '''
    country = df[df['Country Code'] == country_code]
    country_w_codes = country[country['Indicator Code'].isin(indicators)]

    country_w_codes.to_csv(f'data/processed/{country_code}_individual.csv')

    return country_w_codes


def join_df(df, country_codes, indicators):
    '''
    Joins all of the cleaned dataframes into one .csv saved to disk

    Input:
        df - the DataFrames
        indicators - the indicator codes

    Output:
        Returns the joined DataFrame
        Saves the .csv
    '''
    joined = pd.DataFrame(df.iloc[0]).T

    for country in country_codes:
        country_dfs = country_df(df, country, indicators)
        joined = pd.concat([joined, country_dfs], axis=0)

    joined = joined.drop(index=4)\
                   .set_index('Country Name')

    joined.to_csv('data/processed/EdStatsAggregated.csv')

    return joined


def one_indicator_df(df, indicators):
    '''
    Saves a copy of each indicator code we're interested in
    with all the countries we want. Also strips out NaNs.

    Input:
        df - the DataFrame
        indicators - the indicator codes

    Output:
        No return. Just saving the .csv
    '''
    for code in indicators:
        one_code_df = df.copy()
        one_code_df = one_code_df[one_code_df['Indicator Code'] == code]
        one_code_df = one_code_df.reset_index(drop=True)
        one_code_df.to_csv(f'data/processed/{code}.csv')


if __name__ == '__main__':
    with open('data/countries.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
    country_codes = data[0]

    with open('data/indicators.csv') as g:
        reader = csv.reader(g)
        data_ = list(reader)
    indicators = data_[0]
    
    df_to_clean = pd.read_csv('data/raw/EdStatsData.csv')

    clean_df = drop_empty(df_to_clean)

    joined_df = join_df(clean_df, country_codes, indicators)

    one_indicator_df(joined_df, indicators)
