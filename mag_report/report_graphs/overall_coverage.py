import plotly.graph_objects as go
import pandas as pd

from typing import Optional, Union, List

from observatory.reports.abstract_chart import AbstractObservatoryChart


class OverallCoverage(AbstractObservatoryChart):

    def __init__(self,
                 data_dict: dict,
                 line_offset: Optional = None,
                 column_offset: float = 0.1
                 ):

        self.datadict = data_dict
        self.processed_data = False
        self.line_offset = line_offset
        self.column_offset = column_offset

    def process_data(self):
        self.columns = [
            [
                dict(y0=0,
                     y1=self.datadict['total_dois'],
                     line=dict(color='black'),
                     fillcolor='rgba(100, 100, 100, 0.2)'),
                dict(y0=self.datadict['total_dois'],
                     y1=self.datadict['total_objects'],
                     line=dict(color='black'))
            ],
            [
                dict(y0=0,
                     y1=self.datadict['cr_total'],
                     line=dict(color='darkgreen'),
                     fillcolor='rgba(0, 180, 0, 0.2)',
                     line_offset=self.line_offset
                     ),
                dict(y0=self.datadict['cr_not_in_mag'],
                     y1=self.datadict['total_objects'],
                     line=dict(color='darkblue'),
                     fillcolor='rgba(0, 0, 180, 0.2)')
            ]
        ]

        self.labels = dict(
            x=[
                2, 2, *([4 + self.column_offset] * 4)
            ],
            y=[
                self.columns[0][0]['y1'] / 2,
                (self.columns[0][1]['y1'] - self.columns[0][1]['y0']) / 2 + self.columns[0][1]['y0'],
                (self.columns[1][1]['y0'] - self.columns[1][0]['y0']) / 2,
                (self.columns[1][0]['y1'] - self.columns[1][1]['y0']) / 2 + self.columns[1][1]['y0'],
                (self.columns[0][0]['y1'] - self.columns[1][0]['y1']) / 2 + self.columns[1][0]['y1'],
                (self.columns[1][1]['y1'] - self.columns[0][0]['y1']) / 2 + self.columns[0][0]['y1']
            ],
            text=[
                f"Objects with DOIs {int(self.datadict['total_dois'] / 1e6)}M",
                f"Objects without DOIs {int(self.datadict['objects_wo_dois'] / 1e6)}M",
                f"Crossref Only {int(self.datadict['cr_not_in_mag'] / 1e6)}M",
                f"Crossref and MAG {int(self.datadict['cr_in_mag'] / 1e6)}M",
                f"Non-Crossref DOIs in MAG {int(self.datadict['mag_dois_not_cr'] / 1e6)}M",
                f"MAG Only {int(self.datadict['mag_no_doi'] / 1e6)}M"
            ]
        )

    def plot(self, ax=None, fig=None, **kwargs):
        pass

    def plotly(self, fig=None, **kwargs):
        if not self.processed_data:
            self.process_data()

        if not fig:
            fig = go.Figure()

        # Set axes properties
        fig.update_xaxes(range=[0, (2 * len(self.columns) + 2)],
                         visible=False,
                         showgrid=False)
        fig.update_yaxes(range=[0, self.datadict.get('total_objects')],
                         showgrid=False)

        # Add shapes
        for i, column in enumerate(self.columns):
            for rectangle in column:
                if not rectangle.get('line_offset'):
                    rectangle['line_offset'] = 0
                fig.add_shape(type="rect",
                              x0=(i * 2 + 1 - rectangle['line_offset']) + i * self.column_offset,
                              x1=((i + 1) * 2 + 1 + rectangle['line_offset']) + i * self.column_offset,
                              y0=rectangle.get('y0'), y1=rectangle.get('y1'),
                              line=rectangle.get('line'),
                              fillcolor=rectangle.get('fillcolor')
                              )
        fig.update_shapes(dict(xref='x', yref='y'))

        # Add labels
        fig.add_trace(go.Scatter(
            **self.labels,
            mode='text',
            textfont=dict(
                color="black",
                size=18,
                family="Arial"
            ))
        )

        return fig
