import plotly.graph_objects as go
import pandas as pd

from typing import Optional, Union, List  # , Literal

from observatory.reports.abstract_chart import AbstractObservatoryChart


class ValueAddBar(AbstractObservatoryChart):

    def __init__(self,
                 df: pd.DataFrame,
                 categories: [List[str]],
                 xs: List[str],
                 ys: Optional[dict] = None,
                 stackedbar = True
                 ):
        self.df = df
        self.xs = xs
        self.ys = ys
        self.categories = categories
        self.stackedbar = stackedbar
        self.processed_data = False

        if not self.ys:
            self.ys = {
                'Crossref': {
                    'Affiliations': 'pc_dois_with_cr_affiliation_strings',
                    'Abstracts': 'pc_dois_with_cr_abstract',
                    'Citations to': 'pc_dois_with_cr_citations',
                    'References from': 'pc_dois_with_cr_references',
                    'Subjects': 'pc_dois_with_cr_subjects'
                },
                'Microsoft Academic Adds': {
                    'Affiliations': 'pc_dois_mag_aff_string_but_not_cr',
                    'Abstracts': 'pc_dois_with_mag_not_cr_abstract',
                    'Citations to': 'pc_dois_with_mag_not_cr_citations',
                    'References from': 'pc_dois_with_mag_not_cr_references',
                    'Subjects': 'pc_dois_with_mag_field0'
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
        if self.stackedbar:
            fig.update_layout(barmode='stack', template='none')
        fig.update_yaxes(range=[0, 100])
        return fig


class ValueAddByCrossrefType(AbstractObservatoryChart):

    def __init__(self,
                 df: pd.DataFrame,
                 metadata_element: str,
                 ys = None,
                 stackedbar = True
                 ):
        self.df = df
        self.metadata_element = metadata_element
        self.categories = ['Crossref', 'Microsoft Academic Adds']
        self.ys = ys
        self.stackedbar = stackedbar
        self.processed_data = False

        if not self.ys:
            self.ys = {
            'Crossref': {
                'Affiliations': 'pc_dois_with_cr_affiliation_strings',
                'Abstracts': 'pc_dois_with_cr_abstract',
                'Citations to': 'pc_dois_with_cr_citations',
                'References from': 'pc_dois_with_cr_references',
                'Subjects': 'pc_dois_with_cr_subjects'
            },
            'Microsoft Academic Adds': {
                'Affiliations': 'pc_dois_mag_aff_string_but_not_cr',
                'Abstracts': 'pc_dois_with_mag_not_cr_abstract',
                'Citations to': 'pc_dois_with_mag_not_cr_citations',
                'References from': 'pc_dois_with_mag_not_cr_references',
                'Subjects': 'pc_dois_with_mag_field0'
            }
            }

    def process_data(self):

        cr_types = ['journal-article',
                    'proceedings',
                    'book-chapter',
                    'book',
                    'posted-content',
                    'report',
                    'monograph']
        self.figdata = [
            go.Bar(name=category,
                   x=cr_types,
                   y=[self.df[self.df.cr_type == t][
                          self.ys.get(category).get(self.metadata_element)].values[0]
                      for t in cr_types])
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
        if self.stackedbar:
            fig.update_layout(barmode='stack', template='none')
        fig.update_yaxes(range=[0, 100])
        return fig
