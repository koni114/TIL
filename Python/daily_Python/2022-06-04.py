"""
plotly 를 통한
histogram, boxplot, scatter, density plot 그려보기.
"""
import pandas as pd
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

df = pd.read_csv("test_data/iris.csv")

"""
histogram.
전체 양품, 전체 불량, 월별 양품, 월별 불량 데이터를 각각 histogram 에 그려야함.
"""
m_df = pd.read_csv("test_data/iris.csv")
d_df = pd.read_csv("test_data/iris.csv")
d_df.iloc[:, [0, 1, 2, 3]] = d_df.iloc[:, [0, 1, 2, 3]] + 2

m_df = m_df.loc[m_df.variety != "Virginica", :]
d_df = d_df.loc[d_df.variety != "Virginica", :]

m_good_df = m_df.loc[m_df.variety == "Setosa", :]
m_bad_df = m_df.loc[m_df.variety == "Versicolor", :]
d_good_df = d_df.loc[d_df.variety == "Setosa", :]
d_bad_df = d_df.loc[d_df.variety == "Versicolor", :]

x_var = "sepal.length"
fac_var = "variety"


fig = go.Figure()
fig.add_trace(go.Histogram(
    x=m_good_df[x_var].tolist(),
    name="월별 양호",
    marker_color="#A9A9A9",
    opacity=0.75
))


fig.add_trace(go.Histogram(
    x=m_bad_df[x_var].tolist(),
    name="월별 불량",
    marker_color="#C0C0C0",
    opacity=0.75
))


fig.add_trace(go.Histogram(
    x=m_bad_df[x_var].tolist(),
    name="일별 양호",
    marker_color="#af98cf",
    opacity=0.75
))

fig.add_trace(go.Histogram(
    x=m_bad_df[x_var].tolist(),
    name="일별 불량",
    marker_color="#68c182",
    opacity=0.75
))

fig.update_layout(
    title_text='Sampled Results', # title of plot
    xaxis_title_text='Value', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2,      # gap between bars of adjacent location coordinates
    bargroupgap=0.1  # gap between bars of the same location coordinates
)

fig.show()

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = 'AppleGothic'
font_list = [font.name for font in fm.fontManager.ttflist]

##############
## box-plot ##
##############
import pandas as pd
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

m_df = pd.read_csv("test_data/iris.csv")
d_df = pd.read_csv("test_data/iris.csv")
d_df.iloc[:, [0, 1, 2, 3]] = d_df.iloc[:, [0, 1, 2, 3]] + 2

m_df = m_df.loc[m_df.variety != "Virginica", :]
d_df = d_df.loc[d_df.variety != "Virginica", :]

m_good_df = m_df.loc[m_df.variety == "Setosa", :]
m_bad_df = m_df.loc[m_df.variety == "Versicolor", :]
d_good_df = d_df.loc[d_df.variety == "Setosa", :]
d_bad_df = d_df.loc[d_df.variety == "Versicolor", :]

x_var = "sepal.length"
fac_var = "variety"

fig = go.Figure()
fig.add_trace(go.Box(
    y=m_bad_df[x_var].tolist(),
    name="일별 불량",
    marker=dict(color="#68c182"),
    opacity=0.75
))

fig.add_trace(go.Box(
    y=m_bad_df[x_var].tolist(),
    name="일별 양호",
    marker=dict(color="#af98cf"),
    opacity=0.75
))

fig.show()






