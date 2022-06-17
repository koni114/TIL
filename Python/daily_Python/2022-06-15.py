"""
rank plot.
"""
import random
import os
from typing import List

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"
plt.rcParams["font.family"] = 'AppleGothic'


analysis_df = pd.DataFrame({"VAR_NM": ["Slab폭", "Coil두께", "Coil폭", "BlackLine결함수", "Tundishnozzle막힘지수",
                                     "용강과열도", "Slab두께", "Coil길이", "주조평균속도", "탕면변동폭최대치",
                                     "MLAC총Scan횟수", "MLAC_5_mm_적중률"],
                          "TEST_MEAN": [0.00000000, 0.00000000,  0.00000001, 0.00000014,
                                        0.00000043, 0.00000157, 0.00001243, 0.00007523,
                                        0.02939522, 0.13250984, 0.15166854, 0.65223190],
                          "T지표": [random.random() for _ in range(12)],
                          "TEST_INTEL_A": [random.random() for _ in range(12)],
                          "TEST_INTEL_V": [random.random() for _ in range(12)],
                          "CAUSE_RANK": [i+1 for i in range(12)],
                          "CAUSE_YN": ["Y", "Y", "Y", "Y", "Y", "Y", "Y",
                                       "Y", "Y", "N", "N", "N"],
                          "AGGR_DT": ["2022-06-05" for _ in range(12)],
                          "TEST_LOGIT": [None for _ in range(12)],
                          "VAR_ID": ["V4012", "V2986", "V3096", "V2722",
                                     "V1367", "1251", "V3894", "V3207",
                                     "V1962", "1721", "V1841", "D1095"]})

analysis_df["CTQ_ID"] = ["C4109" for _ in range(12)]
x_var_list = ["TEST_MEAN", "TEST_INTEL_A", "TEST_INTEL_V"]
y_var = "VAR_NM"
group_var = ["CTQ_ID"]
fac_var = "CAUSE_YN"
cause_y_color = "#00a5e5"
cause_n_color = "#5b8191"
plot_dir = "Python/daily_Python/plot"
# 정적 PLOT.
# seaborn

class posGetHorizonBar:
    """
        정적, 동적 ranking plot(horizon bar plot)을 만드는 클래스
        - 정적: seaborn
        - 동적: plotly
    """
    def __init__(self, aggr_dt: str, analysis_df: pd.DataFrame, x_var_list: str, y_var: str,
                 group_var: List, fac_var: str, max_std: int, good_label: str,
                 bad_label: str):
        self.aggr_dt = aggr_dt
        self.analysis_df = analysis_df
        self.x_var_list = x_var_list
        self.y_var = y_var
        self.group_var = group_var
        self.fac_var = fac_var
        self.max_std = max_std
        self.cause_y_color = "#00a5e5"
        self.cause_n_color = "#5b8191"

    def get_plot_tp(self, rank_type: str):
        plot_tp_dict = {"TEST_MEAN": "TT",
                        "TEST_INTEL_A": "IA",
                        "TEST_INTEL_V": "IV",
                        "CHITEST": "CT",
                        "ENTRPY": "ET",
                        "BGRATIO": "BG"}
        return plot_tp_dict[rank_type]

    def get_xlab_txt(self, rank_type: str):
        xlab_txt_dict = {"TEST_MEAN": "P-VALUE",
                         "TEST_INTEL_A": "INTEL 평균",
                         "TEST_INTEL_V": "INTEL 분산",
                         "CHITEST": "카이제곱검정",
                         "ENTRPY": "DecisionTree(엔트로피)",
                         "BGRATIO": "DecisionTree(BG_Ratio 검정)"}
        return xlab_txt_dict[rank_type]

    def get_grouped_df(self, group_var: List = None):
        if group_var is None:
            result_df = analysis_df.groupby(self.group_var)
        else:
            result_df = analysis_df.groupby(group_var)
        return result_df

    def get_rank_plot(self):
        if len(self.analysis_df) <= 1:
            return

        plot_tp, ds_tp = "rank", "N"

        for (ctq_id, df_by_group_id) in self.get_grouped_df(group_var):
            print(ctq_id, df_by_group_id)
            # rank_type = x_var_list[0]
            if len(df_by_group_id) < 1:
                continue

            for rank_type in x_var_list:

                plot_nm = ctq_id + "_rank_" + self.get_xlab_txt(rank_type)
                plot_file_nm = os.path.join(plot_dir, plot_nm + ".png")

                color_list = [cause_y_color if v == "Y" else cause_n_color for v in df_by_group_id[fac_var]]
                sns_plot = sns.barplot(x=df_by_group_id[rank_type], y=df_by_group_id[y_var], palette=color_list)

                plt.xlabel(self.get_xlab_txt(rank_type))

                fig = sns_plot.get_figure()
                fig.savefig(plot_nm)

    def get_rank_d_plot(self):
        if len(self.analysis_df) <= 1:
            return

        plot_tp, ds_tp = "rank_D", "N"

        for (ctq_id, df_by_group_id) in self.get_grouped_df(group_var):
            print(ctq_id, df_by_group_id)
            # rank_type = x_var_list[0]

            if len(df_by_group_id) < 1:
                continue

            for rank_type in x_var_list:

                df_by_group_id.sort_values([rank_type], ascending=False, inplace=True)

                plot_nm = ctq_id + "_rank_D_" + self.get_xlab_txt(rank_type)
                plot_file_nm = os.path.join(plot_dir, plot_nm + ".png")
                color_list = [cause_y_color if v == "Y" else cause_n_color for v in df_by_group_id[fac_var]]

                fig = go.Figure(data=[go.Bar(
                    x=df_by_group_id[rank_type],
                    y=df_by_group_id[y_var],
                    orientation='h',
                    marker=dict(
                        color=color_list  # marker color can be a single color value or an iterable
                ))])
                fig.update_layout(title_text=plot_nm,
                                  xaxis_title=self.get_xlab_txt(rank_type))









    def get_mail_rank_plot(self):
        """
            Mail 용 정적 ranking PLOT 생성
        :return:
        """















