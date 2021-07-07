# Alluvial Graph
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

# Generate a one step alluvial plot based on a dataframe with from nodes name in one column
# to nodes names in another and flow values in another, with the following format (names are arbitrary):
#
# from      to      flow
# A         C        1
# A         D       20
# B         C        4
# B         D       43
#
# Self flows are not supported and multi-stage diagrams are not currently supported, combinations of from and to
# labels must be unique

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from observatory.reports.abstract_chart import AbstractObservatoryChart


class Alluvial(AbstractObservatoryChart):

    def __init__(self,
                 df: pd.DataFrame,
                 from_col_name: str,
                 to_col_name: str,
                 flow_values_col: str):

        self.from_col_name = from_col_name
        self.to_col_name = to_col_name
        self.flow_values = flow_values_col

        super().__init__(df)

    def process_data(self, **kwargs):

        from_counts = self.df[[self.from_col_name, self.flow_values]].groupby(self.from_col_name).sum()
        to_counts = self.df[[self.to_col_name, self.flow_values]].groupby(self.to_col_name).sum()

        ordered_from_labels = from_counts.sort_values(self.flow_values, ascending=False).index.values
        ordered_to_labels = to_counts.sort_values(self.flow_values, ascending=False).index.values

        self.node_labels = np.append(ordered_from_labels, ordered_to_labels)

        self.link = {
            'source': [],
            'target': [],
            'value': []
        }

        for f in ordered_from_labels:
            for t in ordered_to_labels:
                vals = self.df[(self.df[self.from_col_name] == f) &
                               (self.df[self.to_col_name] == t)][self.flow_values].values
                if len(vals) == 1:
                    self.link['value'].append(vals[0])
                else:
                    continue

                self.link['source'].append(np.where(self.node_labels == f)[0][0])
                self.link['target'].append(np.where(self.node_labels == t)[0][0])

    def plotly(self, **kwargs):

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=self.node_labels,
                color="blue"
            ),
            link=self.link
        )])

        return fig

    def plot(self):
        pass
