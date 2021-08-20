import plotly.graph_objects as go
import pandas as pd

from typing import Optional, Union, List#, Literal

from observatory.reports.abstract_chart import AbstractObservatoryChart


class ValueAddBar(AbstractObservatoryChart):

    def __init__(self,
                 df: pd.DataFrame,
                 categories: [List[str]],
                 xs: List[str],
                 ys: Optional[dict] = None
                 ):
        self.df = df
        self.xs = xs
        self.ys = ys
        self.categories = categories
        self.processed_data = False

        if not self.ys:
            self.ys = {
                'Crossref': {
                    'Affiliations': 'pc_dois_with_cr_affiliation_strings',
                    'Abstracts': 'pc_dois_with_cr_abstract',
                    'Citations to': 'pc_dois_with_cr_citations',
                    'References from': 'pc_dois_with_cr_references',
                },
                'Microsoft Academic Adds': {
                    'Affiliations': 'pc_dois_mag_aff_string_but_not_cr',
                    'Abstracts': 'pc_dois_with_mag_not_cr_abstract',
                    'Citations to': 'pc_dois_with_mag_not_cr_citations',
                    'References from': 'pc_dois_with_mag_not_cr_references'
                }
            }

    def process_data(self):
        self.figdata = [
            go.Bar(name=category,
                   x=self.xs,
                   y=[self.df[self.ys.get(category).get(xi)].values[0] for xi in self.xs])
            for category in self.categories
        ]
        self.processed_data = True

    def plot(self):
        pass

    def plotly(self,
               **kwargs):
        if not self.processed_data:
            self.process_data()

        fig = go.Figure(data=self.figdata)
        fig.update_layout(barmode='stack')
        return fig


class ValueAddByCrossrefType(AbstractObservatoryChart):

    def __init__(self,
                 df: pd.DataFrame,
                 metadata_element: str #  Union[Literal['Abstracts'],
                 #                         Literal['Affiliations'],
                 #                         Literal['Citations to'],
                 #                         Literal['References from'],
                 #                         Literal['Subjects']]
                 ):
        self.df = df
        self.metadata_element = metadata_element
        self.categories = ['Crossref', 'Microsoft Academic Adds']
        self.processed_data = False

    def process_data(self):
        mapping = {
            'Crossref': {
                'Affiliations': 'pc_dois_with_cr_affiliation_strings',
                'Abstracts': 'pc_dois_with_cr_abstract',
                'Citations to': 'pc_dois_with_cr_citations',
                'References from': 'pc_dois_with_cr_references',
            },
            'Microsoft Academic Adds': {
                'Affiliations': 'pc_dois_mag_aff_string_but_not_cr',
                'Abstracts': 'pc_dois_with_mag_not_cr_abstract',
                'Citations to': 'pc_dois_with_mag_not_cr_citations',
                'References from': 'pc_dois_with_mag_not_cr_references'
            }
        }
        pivot = self.df.pivot(columns='cr_type')
        self.figdata = [
            go.Bar(name=category,
                   x=pivot.columns,
                   y=[pivot[cr_type,
                            mapping.get(category).get(self.metadata_element)].values[0]
                      for cr_type in pivot.columns])
            for category in self.categories
        ]
        self.processed_data = True

    def plot(self):
        pass

    def plotly(self,
               **kwargs):

        if not self.processed_data:
            self.process_data()

        fig = go.Figure(data=self.figdata)
        fig.update_layout(barmode='stack')
        return fig
