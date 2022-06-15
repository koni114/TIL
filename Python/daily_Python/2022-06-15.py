"""
rank plot.
"""

# 정적 PLOT.
# seaborn
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