"""
rank plot.
"""
import pandas as pd
from typing import List

# 정적 PLOT.
# seaborn

class posGetHorizonBar:
    """
        정적, 동적 ranking plot(horizon bar plot)을 만드는 클래스
        - 정적: seaborn
        - 동적: plotly
    """
    def __init__(self, aggr_dt: str, d_df: pd.DataFrame, x_var: str,
                 group_var: List, fac_var: str, good_label: str, bad_label: str):
        self.aggr_dt = aggr_dt
        self.d_df = d_df
        self.x_var = x_var
        self.group_var = group_var
        self.fac_var = fac_var
        self.good_label = good_label
        self.bad_label = bad_label

    def get_grouped_df(self, group_var:List = None):
        if group_var is None:
            result_df = self.d_df.groupby([self.group_var])
        else:
            result_df = self.d_df.groupby([group_var])
        return result_df

    def get_rank_plot(self):
        if len(self.d_df) <= 1:
            return

        plot_tp, plot_tp2, ds_tp = "rank", "S", "N"

        for (ctq_id, vf_id, d_df_group_id) in self.get_grouped_df():

            plot_nm = ctq_id + "_" + vf_id + "_density"











import seaborn as sns
import numpy as np

import plotly.io as pio
pio.renderers.default = "browser"

values = np.array([2, 5, 3, 6, 4, 7, 1])
idx = np.array(list('abcdefg'))
clrs = ["#af98cf" if (x < max(values)) else "#68c182" for x in values ]

sns_plot = sns.barplot(x=values, y=idx, palette=clrs)
fig = sns_plot.get_figure()
fig.savefig("name.png")

# plotly
import plotly.graph_objects as go

colors = ['#68c182',] * 5
colors[1] = '#af98cf'

fig = go.Figure(data=[go.Bar(
    y=['Feature A', 'Feature B', 'Feature C',
       'Feature D', 'Feature E'],
    x=[20, 14, 23, 25, 22],
    orientation='h',
    marker_color=colors  # marker color can be a single color value or an iterable
)])
fig.update_layout(title_text='Least Used Feature')
fig.show()