"""
- scatter plot 그려보기.
  - 정적 PLOT --> seaborn.
  - 동적 PLOT --> plotly
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px

import plotly.io as pio
pio.renderers.default = "browser"

import matplotlib.pyplot as plt
plt.rcParams["font.family"] = 'AppleGothic'


m_df_1 = pd.read_csv("test_data/iris.csv")
d_df_1 = pd.read_csv("test_data/iris.csv")
d_df_1.iloc[:, [0, 1, 2, 3]] = d_df_1.iloc[:, [0, 1, 2, 3]] + 2

m_df_1 = m_df_1.loc[m_df_1.variety != "Virginica", :]
d_df_1 = d_df_1.loc[d_df_1.variety != "Virginica", :]

m_df_1["vf_id"] = "V1001"
d_df_1["vf_id"] = "V1001"

m_df_2 = pd.read_csv("test_data/iris.csv")
d_df_2 = pd.read_csv("test_data/iris.csv")
d_df_2.iloc[:, [0, 1, 2, 3]] = d_df_2.iloc[:, [0, 1, 2, 3]] + 2

m_df_2 = m_df_2.loc[m_df_2.variety != "Virginica", :]
d_df_2 = d_df_2.loc[d_df_2.variety != "Virginica", :]

m_df_2["vf_id"] = "V1002"
d_df_2["vf_id"] = "V1002"

m_df = pd.concat([m_df_1, m_df_2], axis=0)
d_df = pd.concat([d_df_1, d_df_2], axis=0)

vf_id_list = d_df.vf_id.unique().tolist()

y_var = "sepal.length"
fac_var = "variety"
group_var = "vf_id"
bad_label = "Setosa"
good_label = "Versicolor"
good_color = "#68c182"
bad_color = "#af98cf"
hue_col = "구분"

color_dict = {"양호": good_color,
              "불량": bad_color}

#  정적 PLOT --> seaborn.
# vf_id = vf_id_list[0]
for vf_id in vf_id_list:
    d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :].copy()

    if len(d_df_by_vf_id) < 1:
        continue

    df_by_vf_id = pd.DataFrame()

    if len(d_df_by_vf_id) >= 1:
        d_df_by_vf_id[hue_col] = np.where(d_df_by_vf_id[fac_var] == good_label, "양호", "불량")
        df_by_vf_id = d_df_by_vf_id.copy()

    df_by_vf_id.reset_index(inplace=True)

    color_list = [color_dict.get(hue_v) for hue_v in df_by_vf_id[hue_col].unique()]
    sns.set_palette(sns.color_palette(color_list))

    sns_plot = sns.scatterplot(data=df_by_vf_id, x="index", y=y_var, hue=hue_col)
    fig = sns_plot.get_figure()
    fig.savefig("name.png")


# 동적 PLOT --> plotly
# vf_id = vf_id_list[0]
for vf_id in vf_id_list:

    fig = go.Figure()
    d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :]

    if len(d_df_by_vf_id) >= 1:
        d_df_by_vf_id[hue_col] = np.where(d_df_by_vf_id[fac_var] == good_label, "양호", "불량")
        df_by_vf_id = d_df_by_vf_id.copy()
    else:
        continue

    d_df_by_vf_id.reset_index(inplace=True)

    group_labels = sorted(d_df_by_vf_id[hue_col].unique(), reverse=True)

    d_df_by_vf_id.sort_values([hue_col], ascending=False, inplace=True)

    color_list = [color_dict.get(label) for label in group_labels]

    fig = px.scatter(d_df_by_vf_id, x="index", y=y_var,
                     color=hue_col,
                     color_discrete_sequence=color_list)

    fig.show()