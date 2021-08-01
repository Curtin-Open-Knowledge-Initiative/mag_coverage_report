import pandas as pd
import plotly.graph_objects as go

from typing import Union, Optional
from pathlib import Path

def collate_time(df: pd.DataFrame,
                 columns: Union[str, list[str]],
                 year_range: Union[list, tuple]):
    if type(columns) == str:
        columns = [columns]

    if type(year_range) == tuple:
        year_range = range(*year_range)

    filtered = df[df.published_year.isin(year_range)]

    return_df = filtered[['school', 'total_outputs'] + columns].groupby('school').sum()
    return_df.reset_index(inplace=True)
    return_df['published_year'] = f'{year_range[0]}-{year_range[-1]}'

    return return_df

def rci_scatter(df: pd.DataFrame,
                x: Union[str, list[str]],
                y: Union[str, list[str]],
                color: Optional[str] = None,
                title: Optional[str] = None,
                fig: Optional[go.Figure] = None,
                show: Optional[bool] = True,
                **kwargs) -> go.Figure:
    if not fig:
        fig = go.Figure()

    if type(x) == str:
        x = [x]
    if type(y) == str:
        y = [y]

    if len(x) == len(y):
        xys = zip(x, y)

    elif len(x) == 1 and len(y) > 1:
        xys = [(x, ys) for ys in y]

    else:
        raise ValueError('X and Y lists need to be equal lengths or x to be a single variable')

    for xs, ys in xys:
        df['ys'] = [ys] * len(df)
        fig.add_trace(go.Scatter(
            x=df[xs],
            y=df[ys],
            mode='markers',
            marker_color=df[color] if color else None,
            customdata=df[['school', 'published_year', 'ys']],
            hovertemplate=
            """School: %{customdata[0]}
            Year: %{customdata[1]}
            RCI Group: %{customdata[2]}
            x: %{x}
            y: %{y}"""
        ))
    if title:
        fig.update_layout(title=title)
        fig.update_layout(xaxis_title='ERA18 RCI Groups')
        fig.update_layout(yaxis_title='MAG-based RCI Groups')
    if show:
        fig.show()
    return fig

DATA_FOLDER = Path('data_files')
MAIN_SCHOOLS = [
    'Curtin Law School',
    'Curtin Medical School',
    'School of Accounting, Economics and Finance',
    'School of Allied Health',
    'School of Civil and Mechanical Engineering',
    'School of Design and the Built Environment',
    'School of Earth and Planetary Sciences',
    'School of Education',
    'School of Elec Eng, Comp and Math Sci',
    'School of Management & Marketing',
    'School of Media, Creative Arts and Social Inquiry',
    'School of Molecular and Life Sciences',
    'School of Nursing',
    'School of Population Health',
    'WASM Minerals, Energy and Chemical Engineering',
    'Not Assigned'
]

CITATION_SCHOOLS = [
    'Curtin Medical School',
    'School of Allied Health',
    'School of Civil and Mechanical Engineering',
    'School of Earth and Planetary Sciences',
    'School of Elec Eng, Comp and Math Sci',
    'School of Molecular and Life Sciences',
    'School of Nursing',
    'School of Population Health',
    'WASM Minerals, Energy and Chemical Engineering',
]

FIELD_METRIC_COLUMNS = [ #'magy_rci_group_0', 'magy_rci_group_I',
#                         'magy_rci_group_II', 'magy_rci_group_III', 'magy_rci_group_IV',
#                         'magy_rci_group_V', 'magy_rci_group_VI',
                         'magy_centile_1',
                        'magy_centile_5', 'magy_centile_10', 'magy_centile_25',
                        'magy_centile_50', 'magy_centile_other']

JOURNAL_METRIC_COLUMNS = ['rci_group_0', 'rci_group_I',
                          'rci_group_II', 'rci_group_III', 'rci_group_IV',
                          'rci_group_V', 'rci_group_VI', 'mag_centile_1',
                          'mag_centile_5', 'mag_centile_10', 'mag_centile_25',
                          'mag_centile_50', 'mag_centile_other']