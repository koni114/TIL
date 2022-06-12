"""
histogram, scatter, boxplot, density plot
plotly, seaborn 을 통해 그리기.
"""


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
import seaborn as sns

import matplotlib.font_manager as fm
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

# histogram parameter setting.
x_var = "sepal.length"
fac_var = "variety"
group_var = "vf_id"
bad_label = "Setosa"
good_label = "Versicolor"
m_good_color = "#C0C0C0"
m_bad_color = "#A9A9A9"
d_good_color = ""
d_bad_color = ""

# box-plot parameter setting.
y_var = "sepal.length"
fac_var = "variety"
group_var = "vf_id"
bad_label = "Setosa"
good_label = "Versicolor"
good_color = "#68c182"
bad_color = "#af98cf"
hue_col = "구분"

# density parameter setting
x_var = "sepal.length"
fac_var = "variety"
group_var = "vf_id"
bad_label = "Setosa"
good_label = "Versicolor"
good_color = "rgba(175, 152, 207, 0.8)"
bad_color = "rgba(104, 193, 130, 0.8)"
hue_col = "구분"

class posGetDensity:
    """
        정적, 동적 density plot 을 만드는 클래스
        - 정적 seaborn
        - 동적 plotly
    """
    def __init__(self, d_df: pd.DataFrame, x_var: str, group_var: str,
                 fac_var: str, good_label: str, bad_label: str):
        self.d_df = d_df
        self.x_var = x_var
        self.group_var = group_var
        self.fac_var = fac_var
        self.good_label = good_label
        self.bad_label = bad_label
        self.hue_col = "구분"
        self.good_color = "rgba(175, 152, 207, 0.8)"
        self.bad_color = "rgba(104, 193, 130, 0.8)"

    def get_vf_id_list(self):
        m_df_grp_var_uniq = m_df[group_var].unique()
        d_df_grp_var_uniq = d_df[group_var].unique()
        vf_id_list = m_df_grp_var_uniq[np.in1d(m_df_grp_var_uniq, d_df_grp_var_uniq)]
        return vf_id_list

    def get_d_density_plot(self):
        if len(d_df) <= 1:
            return

        color_dict = {"양호": good_color,
                      "불량": bad_color}

        vf_id_list = self.get_vf_id_list()

        # vf_id = vf_id_list[0]
        for vf_id in vf_id_list:

            dist_data = []

            d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :].copy()

            if len(d_df_by_vf_id) < 1:
                continue

            d_df_by_vf_id[hue_col] = np.where(d_df_by_vf_id[fac_var] == good_label, "양호", "불량")

            d_good_df_by_vf_id = d_df_by_vf_id.loc[d_df_by_vf_id[fac_var] == good_label, :].copy()
            d_bad_df_by_vf_id = d_df_by_vf_id.loc[d_df_by_vf_id[fac_var] == bad_label, :].copy()

            if len(d_good_df_by_vf_id) >= 1:
                dist_data.append(d_good_df_by_vf_id[x_var].tolist())

            if len(d_bad_df_by_vf_id) >= 1:
                dist_data.append(d_bad_df_by_vf_id[x_var].tolist())

            group_labels = sorted(d_df_by_vf_id[hue_col].unique(), reverse=True)

            color_list = [color_dict.get(label) for label in group_labels]

            fig_obj = ff.create_distplot(dist_data,
                                         group_labels,
                                         bin_size=1.0,
                                         curve_type="normal",
                                         colors=color_list,
                                         show_hist=False,
                                         show_curve=True,
                                         show_rug=False)




class posGetBox:
    """
        정적, 동적 boxplot 을 만드는 클래스
        - 정적: seaborn
        - 동적: plotly
    """
    def __init__(self, d_df: pd.DataFrame, y_var: str, group_var: str,
                 fac_var: str, good_label: str, bad_label: str):
        self.d_df = d_df
        self.y_var = y_var
        self.group_var = group_var
        self.fac_var = fac_var
        self.good_label = good_label
        self.bad_label = bad_label
        self.hue_col = "구분"
        self.good_color = "#68c182"
        self.bad_color = "#af98cf"

    def get_vf_id_list(self):
        m_df_grp_var_uniq = m_df[group_var].unique()
        d_df_grp_var_uniq = d_df[group_var].unique()
        vf_id_list = m_df_grp_var_uniq[np.in1d(m_df_grp_var_uniq, d_df_grp_var_uniq)]
        return vf_id_list

    def get_box_plot(self):
        if len(d_df) <= 1:
            return

        color_dict = {"양호": good_color,
                      "불량": bad_color}

        vf_id_list = self.get_vf_id_list()
        # vf_id = vf_id_list[0]
        for vf_id in vf_id_list:
            d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :].copy()

            if len(d_df_by_vf_id) < 1:
                continue

            df_by_vf_id = pd.DataFrame()

            if len(d_df_by_vf_id) >= 1:
                d_df_by_vf_id[hue_col] = np.where(d_df_by_vf_id[fac_var] == good_label, "양호", "불량")
                df_by_vf_id = d_df_by_vf_id.copy()

            color_list = [color_dict.get(hue_v) for hue_v in df_by_vf_id[hue_col].unique()]
            sns.set_palette(sns.color_palette(color_list))

            sns_plot = sns.boxplot(data=df_by_vf_id, x=hue_col, y=y_var)
            fig = sns_plot.get_figure()
            fig.savefig("name.png")


    def get_d_box_plot(self):
        if len(d_df) <= 1:
            return

        fig = go.Figure()
        vf_id_list = self.get_vf_id_list()

        # vf_id = vf_id_list[0]
        for vf_id in vf_id_list:

            d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :]

            d_good_df_by_vf_id = d_df_by_vf_id.loc[d_df_by_vf_id[fac_var] == good_label, :]
            d_bad_df_by_vf_id = d_df_by_vf_id.loc[d_df_by_vf_id[fac_var] == bad_label, :]

            # label_name, color, df = ("양호", good_color, d_good_df_by_vf_id)
            for label_name, color, df in [("양호", good_color, d_good_df_by_vf_id),
                                          ("불량", bad_color, d_bad_df_by_vf_id)]:

                if len(df) <= 1:
                    continue

                fig.add_trace(go.Box(
                    y=df[y_var].tolist(),
                    name=label_name,
                    marker=dict(
                        color=color
                    ),
                    opacity=0.75
                ))

            fig.update_layout(
                bargap=0.2,      # gap between bars of adjacent location coordinates
                bargroupgap=0.1  # gap between bars of the same location coordinates
            )

            fig.show()


class posGetHist:
    """
        정적, 동적 histogram 을 만드는 클래스.
            - 정적: seaborn
            - 동적: plotly
    """
    def __init__(self, m_df: pd.DataFrame, d_df: pd.DataFrame,
                 x_var: str, group_var: str, fac_var: str, good_label: str, bad_label: str):
        self.m_df = m_df
        self.d_df = d_df
        self.x_var = x_var
        self.group_var = group_var
        self.fac_var = fac_var
        self.good_label = good_label
        self.bad_label = bad_label
        self.hue_col = "구분"
        self.m_good_color = "#C0C0C0"
        self.m_bad_color = "#A9A9A9"
        self.d_good_color = "#68c182"
        self.d_bad_color = "#af98cf"

    def get_hist_plot(self):
        if len(m_df) <= 1 and len(d_df) <= 1:
            return

        color_dict = {"월별 양호": m_good_color,
                      "월별 불량": m_bad_color,
                      "일별 양호": d_good_color,
                      "일별 불량": d_bad_color}

        vf_id_list = self.get_vf_id_list()
        # vf_id = vf_id_list[0]
        for vf_id in vf_id_list:
            m_df_by_vf_id = m_df.loc[m_df[group_var] == vf_id, :].copy()
            d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :].copy()

            if len(m_df_by_vf_id) < 1 and len(d_df_by_vf_id) < 1:
                continue

            df_by_vf_id = pd.DataFrame()

            if len(m_df_by_vf_id) >= 1:
                m_df_by_vf_id[hue_col] = np.where(m_df_by_vf_id[fac_var] == good_label, "월별 양호", "월별 불량")
                df_by_vf_id = m_df_by_vf_id.copy()

            if len(d_df_by_vf_id) >= 1:
                d_df_by_vf_id[hue_col] = np.where(d_df_by_vf_id[fac_var] == good_label, "일별 양호", "일별 불량")
                if len(df_by_vf_id) < 1:
                    df_by_vf_id = d_df_by_vf_id.copy()
                else:
                    df_by_vf_id = pd.concat([df_by_vf_id, d_df_by_vf_id], axis=0)

            color_list = [color_dict.get(hue_v) for hue_v in df_by_vf_id[hue_col].unique()]
            sns.set_palette(sns.color_palette(color_list))

            sns_plot = sns.histplot(data=df_by_vf_id, x=x_var, hue=hue_col, multiple="dodge")
            fig = sns_plot.get_figure()
            fig.savefig("name.png")

    def get_vf_id_list(self):
        m_df_grp_var_uniq = m_df[group_var].unique()
        d_df_grp_var_uniq = d_df[group_var].unique()
        vf_id_list = m_df_grp_var_uniq[np.in1d(m_df_grp_var_uniq, d_df_grp_var_uniq)]
        return vf_id_list

    def get_d_hist_plot(self):
        if len(m_df) <= 1 and len(d_df) <= 1:
            return

        fig = go.Figure()

        vf_id_list = self.get_vf_id_list()

        # vf_id = vf_id_list[0]
        for vf_id in vf_id_list:

            m_df_by_vf_id = m_df.loc[m_df[group_var] == vf_id, :]
            d_df_by_vf_id = d_df.loc[d_df[group_var] == vf_id, :]

            m_good_df_by_vf_id = m_df_by_vf_id.loc[m_df_by_vf_id[fac_var] == good_label, :]
            m_bad_df_by_vf_id = m_df_by_vf_id.loc[m_df_by_vf_id[fac_var] == bad_label, :]

            d_good_df_by_vf_id = d_df_by_vf_id.loc[d_df_by_vf_id[fac_var] == good_label, :]
            d_bad_df_by_vf_id = d_df_by_vf_id.loc[d_df_by_vf_id[fac_var] == bad_label, :]

            # label_name, color, df = ("월별 양호", m_good_color, m_good_df_by_vf_id)
            for label_name, color, df in [("월별 양호", self.m_good_color, m_good_df_by_vf_id),
                                          ("월별 불량", self.m_bad_color, m_bad_df_by_vf_id),
                                          ("일별 양호", self.d_good_color, d_good_df_by_vf_id),
                                          ("일별 불량", self.d_bad_color, d_bad_df_by_vf_id)]:

                if len(df) <= 1:
                    continue

                fig.add_trace(go.Histogram(
                    x=df[x_var].tolist(),
                    name=label_name,
                    marker=dict(
                        color=color
                    ),
                    opacity=0.75
                ))

            fig.update_layout(
                xaxis_title_text='실적 값',      # xaxis label
                yaxis_title_text='개수',        # yaxis label
                bargap=0.2,      # gap between bars of adjacent location coordinates
                bargroupgap=0.1  # gap between bars of the same location coordinates
            )







































