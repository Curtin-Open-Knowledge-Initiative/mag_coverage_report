import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Union, Optional

from observatory.reports.chart_utils import calculate_percentages
from local_utils import (rci_scatter,
                         collate_time,
                         DATA_FOLDER,
                         MAIN_SCHOOLS,
                         CITATION_SCHOOLS,
                         FIELD_METRIC_COLUMNS,
                         JOURNAL_METRIC_COLUMNS)

oz_field = pd.read_csv(DATA_FOLDER / 'combined_oz_field-norm.csv')
world_field = pd.read_csv(DATA_FOLDER / 'combined_world_field-norm.csv')
go8_field = pd.read_csv(DATA_FOLDER / 'combined_go8_field-norm.csv')
atn_field = pd.read_csv(DATA_FOLDER / 'combined_atn_field-norm.csv')

era18 = pd.read_csv(DATA_FOLDER / 'era18.csv')

collations = []
input_dfs = [world_field, oz_field, go8_field, atn_field]

for df in input_dfs:
    collated = collate_time(df,
                            columns=FIELD_METRIC_COLUMNS,
                            year_range=(2011, 2017))

    for year_range in [(2012, 2018), (2013, 2019), (2014, 2020), (2015, 2021)]:
        coll = collate_time(df,
                                                columns=FIELD_METRIC_COLUMNS,
                                                year_range=year_range)
        collated = collated.append(coll)

    calculate_percentages(collated,
                          numer_columns=FIELD_METRIC_COLUMNS,
                          denom_column='total_outputs')

    collated['percent_above_95'] = collated.percent_magy_centile_5 + collated.percent_magy_centile_1
    collated['percent_above_90'] = collated.percent_magy_centile_10 + collated.percent_above_95
    collated['percent_above_75'] = collated.percent_magy_centile_25 + collated.percent_above_90

    # collated.set_index(['school', 'published_year'], inplace=True)
    # collated = collated.unstack('published_year')
    collated.sort_values(['published_year', 'school'], inplace=True)
    collations.append(collated)

names = [
    'world',
    'australia',
    'go8',
    'atn'
]

comparison = pd.DataFrame({'school': world_field.school.unique()})
comparison.sort_values('school', inplace=True)
comparison.set_index('school', inplace=True)

collations[0].to_csv('global-field-norm.csv')

for i, df in enumerate(collations):

    df_2011_16 = df.loc[df.published_year == '2011-2016']
    df_2011_16.set_index('school', inplace=True)
    df_2015_20 = df[df.published_year == '2015-2020']
    df_2015_20.set_index('school', inplace=True)
    joined = df_2011_16.join(df_2015_20, lsuffix='_11-16', rsuffix='_15-20')

    joined['percent_above_90_change'] = joined['percent_above_90_15-20'] - joined['percent_above_90_11-16']
    joined['percent_above_95_change'] = joined['percent_above_95_15-20'] - joined['percent_above_95_11-16']
    joined['percent_magy_centile_other_change'] = joined['percent_magy_centile_other_15-20'] - joined['percent_magy_centile_other_11-16']

    comparison = comparison.join(joined, lsuffix='', rsuffix=f'_{names[i]}')

for comp in names[1:]:
    for metric in ['percent_above_90', 'percent_above_95', 'percent_magy_centile_other']:
        fig = px.scatter(comparison[comparison.index.isin(MAIN_SCHOOLS)],
                         x=f"{metric}_change",
                         y=f"{metric}_change_{comp}",
                         hover_name=comparison[comparison.index.isin(MAIN_SCHOOLS)].index.values,
                         title=f'Compare {comp}')

        fig.show()

fig = px.scatter(comparison[comparison.index.isin(MAIN_SCHOOLS)],
                         x=f'percent_above_90_11-16',
                         y=f'percent_above_90_15-20',
                         hover_name=comparison[comparison.index.isin(MAIN_SCHOOLS)].index.values,
                         title=f'Compare World')

fig.add_trace(go.Scatter(
    x=[0,40],
    y=[0,40], mode='lines'
))

fig.show()

for comp in names[1:]:
        fig = px.scatter(comparison[comparison.index.isin(MAIN_SCHOOLS)],
                         x=f'percent_above_90_11-16_{comp}',
                         y=f'percent_above_90_15-20_{comp}',
                         hover_name=comparison[comparison.index.isin(MAIN_SCHOOLS)].index.values,
                         title=f'Compare {comp}')
        fig.add_trace(go.Scatter(
            x=[0, 20],
            y=[0, 20], mode='lines'
        ))
        fig.show()

comparison.to_csv(DATA_FOLDER/'full_centiles_comparison.csv')
