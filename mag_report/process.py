# MAG Metadata Coverage Report
#
# Copyright 2020-21 ######
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Cameron Neylon, Bianca Kramer
import json

import pandas as pd
import numpy as np
from typing import Optional, Callable
import plotly.express as px
import plotly.graph_objects as go
from observatory.reports import report_utils
from precipy.analytics_function import AnalyticsFunction
from report_data_processing.sql import *

PROJECT_ID = 'utrecht-university'
MAG_DATA_FILENAME = 'mag_table_data_store.hd5'
CR_DATA_FILENAME = 'doi_table_data_store.hd5'

CURRENT = [2019, 2020, 2021]
LAST_DECADE = range(2010, 2021)


def get_doi_table_data(af: AnalyticsFunction):
    doi_categories = pd.read_gbq(query=doi_table_categories_query,
                                 project_id=PROJECT_ID)

    with pd.HDFStore(CR_DATA_FILENAME) as store:
        store['doi_categories'] = doi_categories

    af.add_existing_file(CR_DATA_FILENAME)


def get_mag_table_data(af: AnalyticsFunction):
    mag_categories = pd.read_gbq(query=mag_table_categories_query,
                                 project_id=PROJECT_ID)

    with pd.HDFStore(MAG_DATA_FILENAME) as store:
        store['mag_categories'] = mag_categories

    af.add_existing_file(MAG_DATA_FILENAME)


def load_cache_data(af: AnalyticsFunction,
                    function_name: Union[str, Callable],
                    element: str,
                    filename: Optional[str] = None):
    """Convenience function for loading preprepared DataFrames from the cache

    :param filename:
    :param function_name:
    :param element: Component of the filecache to load
    :param af

    Downloaded query data is collected as DataFrames and stored in and HDFS store as DataFrames. This
    is a convenient function for reloading data from that frame.
    """

    if callable(function_name):
        afunction_name = function_name.__name__
    else:
        afunction_name = function_name

    store_filepath = af.path_to_cached_file(
        filename, afunction_name)

    with pd.HDFStore(store_filepath) as store:
        if f"/{element}" not in store.keys():
            return None
        df = store[element]

    return df


def mag_coverage_table(af: AnalyticsFunction):
    mag_data = load_cache_data(af,
                               function_name=get_mag_table_data,
                               element='mag_categories',
                               filename=MAG_DATA_FILENAME)

    table_data = mag_data.groupby('mag_type').agg(
        mag_doctype=pd.NamedAgg(column='mag_type', aggfunc='first'),
        num_magids=pd.NamedAgg(column='num_objects', aggfunc='sum'),
        num_dois=pd.NamedAgg(column='num_dois', aggfunc='sum')
    )

    table_data['pc_dois'] = np.round((table_data.num_magids / table_data.num_dois * 100), 1)

    mag_coverage = report_utils.generate_table_data(
        f"Coverage of DOIs in MAG - All Time",
        table_data,
        identifier=None,
        columns=table_data.columns,
        short_column_names=['MAG Doctype', 'Object Count', 'DOIs', 'MAG Records with DOIs (%)'],
        sort_column='Object Count')
    for f in af.generate_file('mag_coverage_table.json'):
        json.dump(mag_coverage_table, f)

    return 'outputs_table.json'


def value_add_tables_graphs(af: AnalyticsFunction):
    cr_data = load_cache_data(af,
                              function_name=get_doi_table_data,
                              element='doi_categories',
                              filename=CR_DATA_FILENAME)

    sum_all = cr_data.sum(axis=0)
    sum_2020 = cr_data[cr_data.published_year == 2020].sum(axis=0)
    sum_current = cr_data[cr_data.published_year.isin(CURRENT)].sum(axis=0)
    sum_lastdecade = cr_data[cr_data.published_year.isin(LAST_DECADE)].sum(axis=0)

    cols = ['dois_with_cr_affiliation_strings',
            'dois_with_cr_orcid',
            'dois_with_cr_abstract',
            'dois_with_cr_subjects',
            'dois_with_cr_citations',
            'dois_with_cr_references',
            'dois_mag_aff_string_but_not_cr',
            'dois_with_mag_author_id_but_not_cr_orcid',
            'dois_with_mag_not_cr_abstract',
            'dois_with_mag_field_not_cr_subject',
            'dois_with_mag_not_cr_citations',
            'dois_more_mag_citations',
            'dois_with_mag_not_cr_references',
            'dois_more_mag_references'
            ]

    summary_table = collate_value_add_values(sum_all, cols)
    summary_table.append(collate_value_add_values(sum_current, cols))
    summary_table.append(collate_value_add_values(sum_2020, cols))

    summary_table['Time Period'] = ['All Time',
                                    'Crossref "Current" (2019-21)',
                                    '2020 Only']

    short_column_names = ['Total DOIs',
                          'CR Affiliation (%)',
                          'CR Abstract (%)',
                          'CR Subject (%)',
                          'CR Citations to (%)',
                          'CR References from (%)',
                          'MAG Added Affiliation String (%)',
                          'MAG Added Author ID (%)',
                          'MAG Added Abstract (%)',
                          'MAG Added Citations (%)',
                          'MAG Higher Citation Count (%)',
                          'MAG Added References (%)',
                          'MAG Higher Reference Count (%)']

    summary_value_add_table = report_utils.generate_table_data('Metadata Coverage and MAG Value Add for Crossref DOIs',
                                                               summary_table,
                                                               columns=['Time Period'] + [f'pc_{col}' for col in cols],
                                                               short_column_names=['Time Period'] + short_column_names,
                                                               identifier_column=None,
                                                               sort_column=None)

    for f in af.generate_file('summary_doi_metadata_coverage.json'):
        json.dump(summary_value_add_table, f)

    sum_by_type = cr_data.groupby('cr_type').sum().reset_index()
    summary_table = collate_value_add_values(sum_by_type)

    summary_value_add_table = report_utils.generate_table_data(
        'Metadata Coverage and MAG Value Add by Crossref Type - All Time',
        summary_table,
        columns=['cr_type'] + [f'pc_{col}' for col in cols],
        short_column_names=['Crossref Type'] + short_column_names,
        identifier_column=None,
        sort_column='Total DOIs',
        sort_ascending=False)

    for f in af.generate_file('summary_doi_metadata_coverage_by_type_alltime.json'):
        json.dump(summary_value_add_table, f)

    sum_2020_by_type = cr_data[cr_data.published_year == 2020].groupby('cr_type').sum().reset_index()
    summary_table = collate_value_add_values(sum_2020_by_type)

    summary_value_add_table = report_utils.generate_table_data(
        'Metadata Coverage and MAG Value Add by Crossref Type - 2020 Publications',
        summary_table,
        columns=['cr_type'] + [f'pc_{col}' for col in cols],
        short_column_names=['Crossref Type'] + short_column_names,
        identifier_column=None,
        sort_column='Total DOIs',
        sort_ascending=False)

    for f in af.generate_file('summary_doi_metadata_coverage_by_type_2020.json'):
        json.dump(summary_value_add_table, f)

    sum_current_by_type = cr_data[cr_data.published_year.isin(CURRENT)].groupby('cr_type').sum().reset_index()
    summary_table = collate_value_add_values(sum_current_by_type)

    summary_value_add_table = report_utils.generate_table_data(
        'Metadata Coverage and MAG Value Add by Crossref Type - Current Period',
        summary_table,
        columns=['cr_type'] + [f'pc_{col}' for col in cols],
        short_column_names=['Crossref Type'] + short_column_names,
        identifier_column=None,
        sort_column='Total DOIs',
        sort_ascending=False)

    for f in af.generate_file('summary_doi_metadata_coverage_by_type_current.json'):
        json.dump(summary_value_add_table, f)



def collate_value_add_values(df: pd.DataFrame,
                             cols: list):
    """
    Convenience function for cleaning up the value add tables
    :param df: summed data frame from the doi_table_categories_query
    :param cols: type: list set of columns to calculate percentages for
    :return df: type: pd.DataFrame modified dataframe with percentages calculated and all columns remaining
    """

    if 'num_dois' not in df.columns:
        df = df.transpose()

    for col in cols:
        df[f'pc_{col}'] = np.round(df[col] / df['num_dois'] * 100, 1)

    return df
