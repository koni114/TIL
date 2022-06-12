"""
이상치 처리 기준 값 생성 클래스.
- data 를 입력 받으면, 이상치 처리에 필요한 값들을 생성.
"""
import math
import pandas as pd
import numpy as np

def is_nan_or_none(x):
    if x is None:
        return True
    if type(x) == float:
        if x != x and math.isnan(x) and pd.isnull(x):
            return True

    return False


pd.set_option("display.max_columns", 100)

rule_df = pd.DataFrame([["01", "M4A_CTQ", "C4109", "V1271",
                         "IQR", 1.5, "B", np.nan, np.nan,
                         "mM", np.nan, np.nan, np.nan,
                         np.nan, np.nan, np.nan],
                        ["01", "M4A_CTQ", "C4109", "V1290",
                         "IQR", 1.5, "B", np.nan, np.nan,
                         "mM", np.nan, np.nan, np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan]],
                       columns=["gcs_comp_code", "biz_op_code", "ds_id", "var_id",
                                "ms_tp", "ms_op", "ms_dir", "ms_lcl", "ms_ucl",
                                "tr_tp", "tr_ucl", "tr_lcl", "tr_v", "attr1", "attr2",
                                "creation_timestamp", "last_update_timestamp", "tr_c"])


df = pd.DataFrame([["2021-07-12", "C4109", "CBU1923", "0" , "V1271", "CBU1923 05", 254.000, np.nan, np.nan, np.nan],
                   ["2021-07-12", "C4109", "CBU1923", "0" , "V1271", "CBU1923 05", 255.000, np.nan, np.nan, np.nan],
                   ["2021-07-12", "C4109", "CBU1923", "0" , "V1271", "CBU1923 05", 256.000, np.nan, np.nan, np.nan]],
                  columns=["aggr_dt", "ctq_id", "ctq_mtl_no", "ctq_result", "vf_id", "mtl_no", "value_n", "value_c",
                           "cpk_ucl", "cpk_lcl"])


stat_df = pd.DataFrame([["C4109",
                         "V1271",
                         69750,
                         df["value_n"].mean(),
                         df["value_n"].std(),
                         df["value_n"].min(),
                         df["value_n"].median(),
                         df["value_n"].max(),
                         df["value_n"].quantile(0.25),
                         df["value_n"].quantile(0.75),
                         13.00,
                         15.00,
                         30.00,
                         32.00,
                         df["value_n"].var(), np.nan, np.nan]],
                       columns=["ctq_id", "vf_id", "CNT", "MEAN_V", "SD_V", "MIN_V", "MEDI_V", "MAX_V", "Q1", "Q3",
                                "PCT05", "PCT10", "PCT90", "PCT95", "VAR_V", "TARGET_V", "CPK_V"])


pd.set_option("display.max_columns", 100)


class posCalNaTreat:
    """
        결측치 처리 Rule 클래스
    """
    def __init__(self, df: pd.DataFrame, rule_df: pd.DataFrame, stat_df: pd.DataFrame):
        self.df = df
        self.rule_df = rule_df
        self.stat_df = stat_df

    def treat_n_df_by_na_treat_rule(self):
        for idx, row in rule_df.iterrows():
            df_by_vf_id = df.loc[np.in1d(df.vf_id, row.var_id), :].copy()
            if len(df_by_vf_id) < 1:
                continue

            if is_nan_or_none(row.tr_tp):
                continue

            if is_nan_or_none(row.tr_v):
                df.loc[np.in1d(df.vf_id, row.var_id), :]["value_n"].dropna(axis=0, inplace=True)
            else:
                ser = df_by_vf_id["value_n"].copy()
                ser[np.isnan(ser)] = row.tr_v
                df.loc[np.in1d(df.vf_id, row.var_id), :]["value_n"] = ser

        return df

    def treat_c_df_by_na_treat_rule(self):
        for idx, row in rule_df.iterrows():
            df_by_vf_id = df.loc[np.in1d(df.vf_id, row.var_id), :].copy()
            if len(df_by_vf_id) < 1:
                continue

            if is_nan_or_none(row.tr_c):
                continue

            ser = df_by_vf_id["value_c"].copy()
            ser[np.isnan(ser)] = row.tr_c
            df.loc[np.in1d(df.vf_id, row.var_id), :]["value_c"] = ser

        return df

    def cal_n_na_treat(self):
        for idx, row in rule_df.iterrows():
            if is_nan_or_none(row.tr_tp):
                continue
            stat_ser = stat_df.loc[np.in1d(stat_df.vf_id, row.var_id), :]
            if len(stat_ser) <= 1:
                continue

            tr_v = np.nan

            if row.tr_tp == "MEAN":
                tr_v = stat_ser.MEAN_V
            elif row.tr_tp == "MEDIAN":
                tr_v = stat_ser.MEDI_V

            stat_df.loc[idx, "tr_v"] = tr_v

    def cal_c_na_treat(self):
        for idx, row in rule_df.iterrows():
            if is_nan_or_none(row.tr_tp):
                continue
            stat_tmp = stat_df.loc[np.in1d(stat_df.vf_id, row.var_id), :]
            if len(stat_tmp) <= 1:
                continue

            if row.ms_tp == "MODE":
                rule_df.loc[idx, "tr_c"] = stat_tmp.sort_values(key=["FCT_VALUE"], ascending=False).loc[0, "FCT_NM"]


class posCalOutlier:
    """
        이상치 기준 Rule 클래스
    """
    def __init__(self, df: pd.DataFrame, rule_df: pd.DataFrame, stat_df: pd.DataFrame):
        self.df = df
        self.rule_df = rule_df
        self.stat_df = stat_df

    def treat_n_df_by_outlier_rule(self):
        """
            이상치 처리 기준 값을 기반으로 수치형 실적 데이터의 이상치를 대체해주는 함수
             측정 유형(ms_tp) --> SP, IQR, SD, PCT, CI, NA
             대체 유형(tr_tp) --> Mm, MEAN, MEDI, DIRT'
             측정 옵션 값(ms_dir). B --> 상하한 둘 다 이상치 처리.  U --> 이상치 상한, L --> 이상치 하한
        :return:
        """
        # idx, row = 0, rule_df.loc[0, :].copy()
        for idx, row in rule_df.iterrows():
            df_by_vf_id = df.loc[np.in1d(df.vf_id, row.var_id), :]
            if len(df_by_vf_id) < 1:
                continue

            if is_nan_or_none(row.ms_tp) or is_nan_or_none(row.tr_tp) or (is_nan_or_none(row.ms_ucl) and is_nan_or_none(row.ms_lcl)):
                continue

            # 측정 유형(ms_tp) --> SP, IQR, SD, PCT, CI, NA
            # 대체 유형(tr_tp) --> Mm, MEAN, MEDI, DIRT
            if row.tr_tp in ["mM", "DIRT"]:
                tr_value = [row.tr_ucl, row.tr_lcl]
            elif row.tr_tp in ["MEAN", "MEDI"]:
                tr_value = row.tr_v
            else:
                continue

            # 측정 옵션 값(ms_dir). B --> 상하한 둘 다 이상치 처리.  U --> 이상치 상한, L --> 이상치 하한
            if is_nan_or_none(row.ms_dir):
                row.ms_dir = "B"

            # 이상치를 상하한 둘 다 처리하는 경우.
            ser = df_by_vf_id["value_n"]
            if row.ms_dir == "B":
                if is_nan_or_none(row.ms_ucl):
                    df_by_vf_id["value_n"] = np.where(ser < row.ms_lcl, tr_value[1], ser)
                elif is_nan_or_none(row.ms_lcl):
                    df_by_vf_id["value_n"] = np.where(ser > row.ms_ucl, tr_value[0], ser)
                else:
                    df_by_vf_id["value_n"] = np.where(ser > row.ms_ucl, tr_value[0], np.where(ser < row.ms_lcl,
                                                                                              tr_value[1],
                                                                                              ser)
                                                      )
            elif row.ms_dir == "U":
                if is_nan_or_none(row.ms_ucl):
                    continue
                df_by_vf_id["value_n"] = np.where(ser < row.ms_lcl, tr_value[1], ser)

            else:
                if is_nan_or_none(row.ms_lcl):
                    continue
                df_by_vf_id["value_n"] = np.where(ser > row.ms_ucl, tr_value[0], ser)

            df.loc[np.in1d(df.vf_id, row.var_id), :] = df_by_vf_id

        return df

    def treat_c_df_by_outlier_rule(self):
        """
            이상치 처리 기준 값을 기반으로 이산형 실적 데이터의 이상치를 대체해주는 함수
        :return:
        """
        for idx, row in rule_df.iterrows():
            df_by_vf_id = df.loc[np.in1d(df.vf_id, row.var_id), :]
            if len(df_by_vf_id) < 1:
                continue

            if is_nan_or_none(row.ms_c) or is_nan_or_none(row.tr_c):
                continue

            ms_c_list = [c.strip() for c in row.ms_c.split(",")]
            ser = df_by_vf_id["value_c"]
            ser[np.in1d(ser, ms_c_list)] = row.tr_c
            df_by_vf_id["value_c"] = ser

            df.loc[np.in1d(df.vf_id, row.var_id), :] = df_by_vf_id

        return df

    def cal_n_outlier_rule(self):
        """
            전체 데이터 통계 데이터를 기반으로 '수치형' 이상치 처리 기준 값 생성 하는 함수.
            ms_tp --> IQR, ms_op --> 1.5
              ms_lcl =  median - (q3 - q1) * 1.5
              ms_ucl =  median + (q3 - q1) * 1.5
            ms_tp --> IQR, ms_op --> 1.8
              ms_lcl =  median - (q3 - q1) * 1.8
              ms_ucl =  median + (q3 - q1) * 1.8
            ms_tp --> PCT, ms_op --> 90
              ms_lcl =  백분율 기준 하위 10%
              ms_ucl =  백분율 기준 상위 10%
            ms_tp --> PCT, ms_op --> 95
              ms_lcl =  백분율 기준 하위 5%
              ms_ucl =  백분율 기준 상위 5%
        """
        # row = rule_df.loc[0, :]
        # idx = 0
        for idx, row in rule_df.iterrows():
            stat_ser = stat_df.loc[np.in1d(stat_df.vf_id, row.var_id), :]
            if len(stat_ser) < 1:
                continue

            if row.ms_tp == "IQR":
                iqr_v = (stat_ser.Q3 - stat_ser.Q1) * row.ms_op
                rule_df.loc[idx, "ms_lcl"] = float(stat_ser.MEDI_V - iqr_v)
                rule_df.loc[idx, "ms_ucl"] = float(stat_ser.MEDI_V + iqr_v)
            elif row.ms_tp == "PCT":
                if row.ms_op == 90 or row.ms_op == "90":
                    rule_df.loc[idx, "ms_lcl"] = float(stat_ser.PCT_10)
                    rule_df.loc[idx, "ms_ucl"] = float(stat_ser.PCT_90)
                else:
                    rule_df.loc[idx, "ms_lcl"] = float(stat_ser.PCT_05)
                    rule_df.loc[idx, "ms_ucl"] = float(stat_ser.PCT_95)

    def cal_c_outlier_rule(self):
        """
            전체 데이터 통계 데이터를 기반으로 '이산형' 이상치 처리 기준 값 생성 하는 함수.
        :return:
        """
        for idx, row in rule_df.iterrows():
            stat_tmp = stat_df.loc[np.in1d(stat_df.vf_id, row.var_id), :]

            if len(stat_tmp) < 1 or np.nan(row.ms_tp) or np.nan(row.ms_op) or np.nan(row.tr_tp):
                continue

            if row.ms_tp == "RMRT":
                if row.ms_op == "01" or row.ms_op == 1:
                    rmrt = stat_tmp.loc[(stat_tmp.FCT_VALUE / stat_tmp.CNT) < 0.01, :]
                else:
                    rmrt = stat_tmp.loc[(stat_tmp.FCT_VALUE / stat_tmp.CNT) < 0.05, :]

                if len(rmrt) >= 1:
                    rule_df.loc[idx, "ms_c"] = ",".join(rmrt.FCT_NM)


    def cal_n_treat_rule(self):
        """
            실적 데이터를 기반으로 '수치형' 이상치 처리 기준 값 생성 하는 함수.
        :return:
        """
        # idx, row = 0 , rule_df.loc[0, ]
        for idx, row in rule_df.iterrows():
            df_tmp = df[df.vf_id == rule_df.loc[idx, "var_id"]]

            if len(df_tmp) < 1:
                continue

            if np.isnan(rule_df.loc[idx, "ms_lcl"]) or np.isnan(rule_df.loc[idx, "ms_ucl"]):
                continue

            df_tmp = df_tmp.loc[(df_tmp["value_n"] <= rule_df.loc[idx, "ms_ucl"])
                                & (df_tmp["value_n"] >= rule_df.loc[idx, "ms_lcl"]), :]

            if len(df_tmp) <= 1:
                continue

            rule_df.loc[idx, "tr_lcl"] = np.round(np.min(df_tmp["value_n"]), 8)
            rule_df.loc[idx, "tr_ucl"] = np.round(np.max(df_tmp["value_n"]), 8)
            rule_df.loc[idx, "tr_v"] = np.round(np.mean(df_tmp["value_n"]), 8)

    def cal_c_treat_rule(self):
        """
            실적 데이터를 기반으로 '이산형' 이상치 처리 기준 값 생성 하는 함수.
        :return:
        """

        for idx, row in rule_df.iterrows():
            stat_tmp = stat_df.loc[np.in1d(stat_df.vf_id, row.var_id), :]

            if row.ms_tp == "MODE":
                rule_df.loc[idx, "tr_c"] = stat_tmp.sort_values(key=["FCT_VALUE"], ascending=False).loc[0, "FCT_NM"]


























































