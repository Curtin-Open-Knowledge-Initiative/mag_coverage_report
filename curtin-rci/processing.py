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
oz_journal = pd.read_csv(DATA_FOLDER / 'combined_oz_journal-norm.csv')
world_journal = pd.read_csv(DATA_FOLDER / 'combined_world_journal-norm.csv')
era18 = pd.read_csv(DATA_FOLDER / 'era18.csv')

oz_field_2011_16 = collate_time(oz_field, columns=FIELD_METRIC_COLUMNS, year_range=(2011, 2017))
world_field_2011_16 = collate_time(world_field, columns=FIELD_METRIC_COLUMNS, year_range=(2011, 2017))
world_journal_2011_16 = collate_time(world_journal, columns=JOURNAL_METRIC_COLUMNS, year_range=(2011, 2017))
world_field_2015_20 = collate_time(world_field, columns=FIELD_METRIC_COLUMNS, year_range=(2015, 2021))
oz_field_2015_20 = collate_time(oz_field, columns=FIELD_METRIC_COLUMNS, year_range=(2015, 2021))

calculate_percentages(era18,
                      numer_columns=['0', 'I', 'II', 'III', 'IV', 'V', 'VI'],
                      denom_column='total_outputs')

for df in [oz_field, world_field, oz_field_2011_16, world_field_2011_16, world_field_2015_20, oz_field_2015_20]:
    calculate_percentages(df=df,
                          numer_columns=FIELD_METRIC_COLUMNS,
                          denom_column='total_outputs')
    df['percent_above_95'] = df.percent_magy_centile_5 + df.percent_magy_centile_1
    df['percent_above_90'] = df.percent_magy_centile_10 + df.percent_above_95
    df['percent_above_75'] = df.percent_magy_centile_25 + df.percent_above_90
    df['percent_rci_v_vi'] = df.percent_magy_rci_group_V + df.percent_magy_rci_group_VI
    df['percent_rci_iv_v_vi'] = df.percent_rci_v_vi + df.percent_magy_rci_group_IV
    df['percent_rci_iii_iv_v_vi'] = df.percent_rci_iv_v_vi + df.percent_magy_rci_group_III

for df in [oz_journal, world_journal, world_journal_2011_16]:
    calculate_percentages(df=df,
                          numer_columns=JOURNAL_METRIC_COLUMNS,
                          denom_column='total_outputs')

    df['percent_above_95'] = df.percent_mag_centile_5 + df.percent_mag_centile_1
    df['percent_above_90'] = df.percent_mag_centile_10 + df.percent_above_95
    df['percent_above_75'] = df.percent_mag_centile_25 + df.percent_above_90
    df['percent_rci_v_vi'] = df.percent_rci_group_V + df.percent_rci_group_VI
    df['percent_rci_iv_v_vi'] = df.percent_rci_v_vi + df.percent_rci_group_IV
    df['percent_rci_iii_iv_v_vi'] = df.percent_rci_iv_v_vi + df.percent_rci_group_III

comp = pd.merge(world_field, era18, on='school', how='left')
comp.sort_values('published_year', inplace=True)

collate_comp = pd.merge(world_field_2011_16, era18, on='school', how='left')
collate_comp.to_csv(DATA_FOLDER / 'ERA to MAG World-Field Normalised Comparing ERA18 Output Years.csv')

collate_jrnl = pd.merge(world_journal_2011_16, era18, on='school', how='left')
collate_jrnl.to_csv(DATA_FOLDER / 'ERA to MAG World-Journal Normalised Comparing ERA18 Output Years.csv')

figdata1 = comp[(comp.published_year.isin(range(2011, 2017))) &
                (comp.school.isin(CITATION_SCHOOLS))]

fig1 = rci_scatter(figdata1,
                   x=['percent_0', 'percent_I', 'percent_II', 'percent_III', 'percent_IV', 'percent_V', 'percent_VI'],
                   y=['percent_magy_rci_group_0',
                      'percent_magy_rci_group_I',
                      'percent_magy_rci_group_II',
                      'percent_magy_rci_group_III',
                      'percent_magy_rci_group_IV',
                      'percent_magy_rci_group_V',
                      'percent_magy_rci_group_VI'],
                   title='Proportion in RCI Groups Comparing ERA18 to MAG-World-Field for Each Year 2011-16',
                   show=False)

fig1.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines'
))

fig1.show()
fig1.write_html('proportion_of_rci_groups_comparison(world-field-eachyear).html')

figdata1[['school', 'published_year', 'total_outputs_x',
          '0', 'I', 'II', 'III', 'IV', 'V', 'VI',
          'percent_0', 'percent_I', 'percent_II', 'percent_III', 'percent_IV', 'percent_V', 'percent_VI',
          'magy_rci_group_0', 'magy_rci_group_I', 'magy_rci_group_II', 'magy_rci_group_III',
          'magy_rci_group_IV', 'magy_rci_group_V', 'magy_rci_group_VI',
          'percent_magy_rci_group_0', 'percent_magy_rci_group_I', 'percent_magy_rci_group_II',
          'percent_magy_rci_group_III',
          'percent_magy_rci_group_IV', 'percent_magy_rci_group_V', 'percent_magy_rci_group_VI']].to_csv(
    DATA_FOLDER / 'ERA to MAG World-Field Normalised by Year.csv')

figdata2 = collate_comp[(collate_comp.school.isin(CITATION_SCHOOLS))]
figdata2['cum_pc_era0'] = figdata2.percent_0
figdata2['cum_pc_eraI'] = figdata2.cum_pc_era0 + figdata2.percent_I
figdata2['cum_pc_eraII'] = figdata2.cum_pc_eraI + figdata2.percent_II
figdata2['cum_pc_eraIII'] = figdata2.cum_pc_eraII + figdata2.percent_III
figdata2['cum_pc_eraIV'] = figdata2.cum_pc_eraIII + figdata2.percent_IV
figdata2['cum_pc_eraV'] = figdata2.cum_pc_eraIV + figdata2.percent_V
figdata2['cum_pc_eraVI'] = figdata2.cum_pc_eraV + figdata2.percent_VI

figdata2['cum_pc_mag0'] = figdata2.percent_magy_rci_group_0
figdata2['cum_pc_magI'] = figdata2.cum_pc_mag0 + figdata2.percent_magy_rci_group_I
figdata2['cum_pc_magII'] = figdata2.cum_pc_magI + figdata2.percent_magy_rci_group_II
figdata2['cum_pc_magIII'] = figdata2.cum_pc_magII + figdata2.percent_magy_rci_group_III
figdata2['cum_pc_magIV'] = figdata2.cum_pc_magIII + figdata2.percent_magy_rci_group_IV
figdata2['cum_pc_magV'] = figdata2.cum_pc_magIV + figdata2.percent_magy_rci_group_V
figdata2['cum_pc_magVI'] = figdata2.cum_pc_magV + figdata2.percent_magy_rci_group_VI

fig1 = rci_scatter(figdata2,
                   x=['0', 'I', 'II', 'III', 'IV', 'V', 'VI'],
                   y=['magy_rci_group_0',
                      'magy_rci_group_I',
                      'magy_rci_group_II',
                      'magy_rci_group_III',
                      'magy_rci_group_IV',
                      'magy_rci_group_V',
                      'magy_rci_group_VI'],
                   title='Number in RCI Groups Comparing ERA18 to MAG-World-Field Combined Over 2011-16',
                   show=False)

fig1.add_trace(go.Scatter(
    x=[0, 900],
    y=[0, 900],
    mode='lines'
))
fig1.show()

fig1.write_html('number_by_rci_group_comparison(world-field-2011-16combined).html')

fig2 = rci_scatter(figdata2,
                   x=['cum_pc_era0', 'cum_pc_eraI', 'cum_pc_eraII', 'cum_pc_eraIII', 'cum_pc_eraIV', 'cum_pc_eraV',
                      'cum_pc_eraVI'],
                   y=['cum_pc_mag0',
                      'cum_pc_magI',
                      'cum_pc_magII',
                      'cum_pc_magIII',
                      'cum_pc_magIV',
                      'cum_pc_magV',
                      'cum_pc_magVI'],
                   title='Cumulative Proportion in RCI Groups Comparing ERA18 to MAG-World-Field Combined Over 2011-16',
                   show=False)

fig2.add_trace(go.Scatter(
    x=[0, 100],
    y=[0, 100],
    mode='lines'
))

fig2.show()
fig2.write_html('cumulative_proportion_by_rci_group_comparison(world-field-2011-16combined).html')

fig2 = rci_scatter(figdata2,
                   x=['percent_0', 'percent_I', 'percent_II', 'percent_III', 'percent_IV', 'percent_V', 'percent_VI'],
                   y=['percent_magy_rci_group_0',
                      'percent_magy_rci_group_I',
                      'percent_magy_rci_group_II',
                      'percent_magy_rci_group_III',
                      'percent_magy_rci_group_IV',
                      'percent_magy_rci_group_V',
                      'percent_magy_rci_group_VI'],
                   title='Proportion in RCI Groups Comparing ERA18 to MAG-World-Field Combined Over 2011-16',
                   show=False)

fig2.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines'
))

fig2.show()
fig2.write_html('proportion_by_rci_group_comparison(world-field-2011-16combined).html')

figdata2[['school', 'published_year', 'total_outputs_x',
          '0', 'I', 'II', 'III', 'IV', 'V', 'VI',
          'percent_0', 'percent_I', 'percent_II', 'percent_III', 'percent_IV', 'percent_V', 'percent_VI',
          'magy_rci_group_0', 'magy_rci_group_I', 'magy_rci_group_II', 'magy_rci_group_III',
          'magy_rci_group_IV', 'magy_rci_group_V', 'magy_rci_group_VI',
          'percent_magy_rci_group_0', 'percent_magy_rci_group_I', 'percent_magy_rci_group_II',
          'percent_magy_rci_group_III',
          'percent_magy_rci_group_IV', 'percent_magy_rci_group_V', 'percent_magy_rci_group_VI'
          ]].to_csv(DATA_FOLDER / 'ERA to MAG World-Field Normalised Comparing ERA18 Output Years.csv')

figdata3 = collate_jrnl[collate_jrnl.school.isin(CITATION_SCHOOLS)]

fig3 = rci_scatter(figdata3,
                   x=['percent_0', 'percent_I', 'percent_II', 'percent_III', 'percent_IV', 'percent_V', 'percent_VI'],
                   y=['percent_rci_group_0',
                      'percent_rci_group_I',
                      'percent_rci_group_II',
                      'percent_rci_group_III',
                      'percent_rci_group_IV',
                      'percent_rci_group_V',
                      'percent_rci_group_VI'],
                   title='Proportion in RCI Groups Comparing ERA18 to MAG-World-Journal Combined Over 2011-16',
                   show=False)

fig3.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines'
))
fig3.show()

figdata4 = pd.merge(world_field_2011_16, world_field_2015_20, on='school', suffixes=['_11-16', '_15-20'])

fig4 = px.scatter(figdata4[figdata4.school.isin(MAIN_SCHOOLS)],
                  x='percent_above_90_11-16',
                  y='percent_above_90_15-20',
                  hover_name='school')
fig4.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines')
)
fig4.show()

fig4 = px.scatter(figdata4[figdata4.school.isin(MAIN_SCHOOLS)],
                  x='percent_above_95_11-16',
                  y='percent_above_95_15-20',
                  hover_name='school')
fig4.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines')
)
fig4.show()

figdata5 = pd.merge(oz_field_2011_16, oz_field_2015_20, on='school', suffixes=['_11-16', '_15-20'])

fig5 = px.scatter(figdata5[figdata5.school.isin(MAIN_SCHOOLS)],
                  x='percent_above_90_11-16',
                  y='percent_above_90_15-20',
                  hover_name='school')
fig5.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines')
)
fig5.show()

fig5 = px.scatter(figdata5[figdata5.school.isin(MAIN_SCHOOLS)],
                  x='percent_above_95_11-16',
                  y='percent_above_95_15-20',
                  hover_name='school')
fig5.add_trace(go.Scatter(
    x=[0, 50],
    y=[0, 50],
    mode='lines')
)
fig4.show()

fig6 = px.line(world_field[(world_field.school.isin(MAIN_SCHOOLS)) &
                           (world_field.published_year.isin(range(2011, 2020)))],
               x='published_year',
               y='percent_above_90',
               color='school',
               title='World-Field, pp10')
fig6.show()

# fig = px.scatter(comp[comp.published_year.isin(range(2011, 2017))],
#                  x='% > world class',
#                  y='percent_rci_iii_iv_v_vi',
#                  color='published_year',
#                  title='World Field 2011-16 vs ERA % World Class',
#                  hover_data=['published_year', 'school'])
#
# fig.add_trace(go.Scatter(
#     x=comp[comp.published_year.isin(range(2011, 2017))]['Top 25%'],
#     y=comp[comp.published_year.isin(range(2011, 2017))]['percent_rci_iv_v_vi'],
#     mode='markers',
#     marker_color=comp[comp.published_year.isin(range(2011, 2017))]['published_year'],
#     text=comp[comp.published_year.isin(range(2011, 2017))]['school']
# )
# )
#
# fig.add_trace(go.Scatter(
#     x=comp[comp.published_year.isin(range(2011, 2017))]['top 10% (excellent)'],
#     y=comp[comp.published_year.isin(range(2011, 2017))]['percent_rci_v_vi'],
#     mode='markers',
#     marker_color=comp[comp.published_year.isin(range(2011, 2017))]['published_year'],
#     text=comp[comp.published_year.isin(range(2011, 2017))]['school']
# )
# )
#
# fig.add_trace(go.Scatter(
#     x=[0, 60],
#     y=[0, 60],
#     mode='lines'
# ))
#
# fig.show()
#
# comp = pd.merge(oz_field, era18, on='school', how='left')
# comp.sort_values('published_year', inplace=True)
#
# fig = px.scatter(comp[comp.published_year.isin(range(2011, 2017))],
#                  x='% > world class',
#                  y='percent_rci_iii_iv_v_vi',
#                  color='published_year',
#                  title='Australian Corpus Field 2011-16 vs ERA % World Class',
#                  hover_data=['published_year', 'school'])
#
# fig.add_trace(go.Scatter(
#     x=comp[comp.published_year.isin(range(2011, 2017))]['Top 25%'],
#     y=comp[comp.published_year.isin(range(2011, 2017))]['percent_rci_iv_v_vi'],
#     mode='markers',
#     marker_color=comp[comp.published_year.isin(range(2011, 2017))]['published_year'],
#     text=comp[comp.published_year.isin(range(2011, 2017))]['school']
# )
# )
#
# fig.add_trace(go.Scatter(
#     x=comp[comp.published_year.isin(range(2011, 2017))]['top 10% (excellent)'],
#     y=comp[comp.published_year.isin(range(2011, 2017))]['percent_rci_v_vi'],
#     mode='markers',
#     marker_color=comp[comp.published_year.isin(range(2011, 2017))]['published_year'],
#     text=comp[comp.published_year.isin(range(2011, 2017))]['school']
# )
# )


# fig1 = px.line(oz_field[(oz_field.published_year.isin(range(2010, 2022))) &
#                         (oz_field.school.isin(MAIN_SCHOOLS))],
#                x='published_year',
#                y='percent_above_90',
#                color='school',
#                title="Oz Field Normalised")
# fig1.show()
#
# fig2 = px.line(world_field[(world_field.published_year.isin(range(2010, 2022))) &
#                            (world_field.school.isin(MAIN_SCHOOLS))],
#                x='published_year',
#                y='percent_above_90',
#                color='school',
#                title="World Field Normalised")
# fig2.show()
#
# fig1 = px.line(oz_journal[(oz_journal.published_year.isin(range(2010, 2022))) &
#                           (oz_journal.school.isin(MAIN_SCHOOLS))],
#                x='published_year',
#                y='percent_above_90',
#                color='school',
#                title="Oz Journal Normalised")
# fig1.show()
#
# fig2 = px.line(world_journal[(world_journal.published_year.isin(range(2010, 2022))) &
#                              (world_journal.school.isin(MAIN_SCHOOLS))],
#                x='published_year',
#                y='percent_above_90',
#                color='school',
#                title="World Journal Normalised")
# fig2.show()
#
# fig3 = px.bar(oz_field[(oz_field.published_year.isin(range(2015, 2021))) &
#                        (oz_field.school.isin(MAIN_SCHOOLS))],
#               x='school',
#               y=[
#                   'percent_magy_rci_group_0',
#                   'percent_magy_rci_group_I',
#                   'percent_magy_rci_group_II',
#                   'percent_magy_rci_group_III',
#                   'percent_magy_rci_group_IV',
#                   'percent_magy_rci_group_V',
#                   'percent_magy_rci_group_VI'],
#               facet_row='published_year',
#               title='Oz Field')
# fig3.show()
#
# fig3 = px.bar(world_field[(world_field.published_year.isin(range(2015, 2021))) &
#                           (world_field.school.isin(MAIN_SCHOOLS))],
#               x='school',
#               y=[
#                   'percent_magy_rci_group_0',
#                   'percent_magy_rci_group_I',
#                   'percent_magy_rci_group_II',
#                   'percent_magy_rci_group_III',
#                   'percent_magy_rci_group_IV',
#                   'percent_magy_rci_group_V',
#                   'percent_magy_rci_group_VI'],
#               facet_row='published_year',
#               title='World Field')
# fig3.show()
#
# # fig4 = px.bar(oz_field[(oz_field.published_year.isin(range(2015, 2021))) &
# #                              (oz_field.school.isin(MAIN_SCHOOLS))],
# #               x='school',
# #               y=[
# #                  'percent_magy_centile_other',
# #                  'percent_magy_centile_50',
# #                  'percent_magy_centile_25',
# #                  'percent_magy_centile_10',
# #                  'percent_magy_centile_5',
# #                  'percent_magy_centile_1'],
# #               facet_row='published_year',
# #               title='Elements-field')
# # fig4.show()
# #
# # fig5 = px.bar(elements_container[(elements_container.published_year.isin(range(2015, 2021))) &
# #                              (elements_container.school.isin(MAIN_SCHOOLS))],
# #               x='school',
# #               y=[
# #                  'percent_mag_centile_other',
# #                  'percent_mag_centile_50',
# #                  'percent_mag_centile_25',
# #                  'percent_mag_centile_10',
# #                  'percent_mag_centile_5',
# #                  'percent_mag_centile_1'],
# #               facet_row='published_year',
# #               title='Elements-Container')
# # fig5.show()
# #
# # fig6 = px.bar(world_field[(world_field.published_year.isin(range(2015, 2021))) &
# #                              (world_field.school.isin(MAIN_SCHOOLS))],
# #               x='school',
# #               y=[
# #                  'percent_magy_centile_other',
# #                  'percent_magy_centile_50',
# #                  'percent_magy_centile_25',
# #                  'percent_magy_centile_10',
# #                  'percent_magy_centile_5',
# #                  'percent_magy_centile_1'],
# #               facet_row='published_year',
# #               title='MAG-Field')
# # fig6.show()
# #
# # fig7 = px.bar(mag_container[(mag_container.published_year.isin(range(2015, 2021))) &
# #                              (mag_container.school.isin(MAIN_SCHOOLS))],
# #               x='school',
# #               y=[
# #                  'percent_mag_centile_other',
# #                  'percent_mag_centile_50',
# #                  'percent_mag_centile_25',
# #                  'percent_mag_centile_10',
# #                  'percent_mag_centile_5',
# #                  'percent_mag_centile_1'],
# #               facet_row='published_year',
# #               title='MAG-Container')
# # fig7.show()
#
# # fig8 = px.line(world_field[(world_field.published_year.isin(range(2015, 2021))) &
# #                          (world_field.school.isin(MAIN_SCHOOLS))],
# #                x='published_year',
# #                y='percent_above_95',
# #                color='school',
# #                title='MAG Field - pc above 95-percentile')
# #
# # fig8.show()
# #
# # fig9 = px.line(mag_container[(mag_container.published_year.isin(range(2015, 2021))) &
# #                              (mag_container.school.isin(MAIN_SCHOOLS))],
# #                x='published_year',
# #                y='percent_above_95',
# #                color='school',
# #                title='MAG Container - pc above 95-percentile')
# #
# # fig9.show()
# #
# # fig8 = px.line(oz_field[(oz_field.published_year.isin(range(2015, 2021))) &
# #                               (oz_field.school.isin(MAIN_SCHOOLS))],
# #                x='published_year',
# #                y='percent_above_95',
# #                color='school',
# #                title='Elements by Field - pc above 95-percentile')
# #
# # fig8.show()
# #
# # fig9 = px.line(elements_container[(elements_container.published_year.isin(range(2015, 2021))) &
# #                                   (elements_container.school.isin(MAIN_SCHOOLS))],
# #                x='published_year',
# #                y='percent_above_95',
# #                color='school',
# #                title='Elements by Container - pc above 95-percentile')
# #
# # fig9.show()
# #
# # figdata = world_field[(world_field.published_year.isin(range(2015, 2021))) &
# #                              (world_field.school.isin(MAIN_SCHOOLS))].sort_values('published_year',
# #                                                                                 ascending=True)
# # fig10 = px.scatter(figdata,
# #                    x='percent_above_90',
# #                    y='percent_above_95',
# #                    color='school',
# #                    size='total_outputs',
# #                    animation_frame='published_year',
# #                    animation_group='school',
# #                    title='MAG by Field')
# # fig10.show()
# #
# # figdata = mag_container[(mag_container.published_year.isin(range(2015, 2021))) &
# #                              (mag_container.school.isin(MAIN_SCHOOLS))].sort_values('published_year',
# #                                                                                 ascending=True)
# #
# # fig11 = px.scatter(figdata,
# #                    x='percent_above_90',
# #                    y='percent_above_95',
# #                    color='school',
# #                    size='total_outputs',
# #                    animation_frame='published_year',
# #                    animation_group='school',
# #                    title='MAG by Container')
# # fig11.show()
#
# # joined = pd.merge(world_field, world_container,
# #                   on=['published_year', 'school'],
# #                   suffixes=['_field', '_container'])
# #
# # working = joined[['published_year',
# #                   'school',
# #                   'total_outputs_field',
# #                   'percent_above_95_field',
# #                   'percent_above_95_container',
# #                   'percent_above_90_field',
# #                   'percent_above_90_container',
# #                   'percent_above_75_field',
# #                   'percent_above_75_container',
# #                   'percent_rci_v_vi_field',
# #                   'percent_rci_v_vi_container',
# #                   'percent_rci_iv_v_vi_field',
# #                   'percent_rci_iv_v_vi_container'
# #                   ]]
# #
# # working.to_csv(DATA_FOLDER / 'summarised.csv')
#
# # figdata = joined[(joined.published_year.isin(range(2015,2021))) &
# #                           (joined.school.isin(MAIN_SCHOOLS))].sort_values('published_year')
# # fig12 = px.scatter(figdata,
# #                    x='percent_above_90_field',
# #                    y='percent_above_90_container',
# #                    size='total_outputs_field',
# #                    color='school',
# #                    animation_frame='published_year',
# #                    animation_group='school')
# #
# # fig12.show()
# #
# # num_comp = pd.merge(oz_field, world_field,
# #                     on=['published_year', 'school'],
# #                     suffixes=['_elements', '_mag'])
# # fig13 = px.scatter(num_comp,
# #                    x='total_outputs_elements',
# #                    y='total_outputs_mag',
# #                    size='percent_above_90_mag',
# #                    color='school')
# # fig13.show()
