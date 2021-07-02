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

import pandas as pd
from precipy.analytics_function import AnalyticsFunction
from report_data_processing.sql import *

PROJECT_ID = 'utrecht-university'

def get_doi_table_data(af: AnalyticsFunction):
    doi_types = pd.read_gbq(query=doi_table_types,
                            project_id=PROJECT_ID)

    doi_categories = pd.read_gbq(query=doi_table_categories_query,
                                 project_id=PROJECT_ID)

    with pd.HDFStore('doi_table_data_store.hd5') as store:
        store['doi_types'] = doi_types
        store['doi_categories'] = doi_categories

    af.add_existing_file('doi_table_data_store.hd5')


def get_mag_table_data(af: AnalyticsFunction):
    mag_types = pd.read_gbq(query=mag_table_types,
                            project_id=PROJECT_ID)
    mag_categories = pd.read_gbq(query=mag_table_categories_query,
                                 project_id=PROJECT_ID)

    with pd.HDFStore('mag_table_data_store.hd5') as store:
        store['mag_types'] = mag_types
        store['mag_categories'] = mag_categories

    af.add_existing_file('mag_table_data_store.hd5')

