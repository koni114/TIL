# 2022-06-18.py
# 이산형 데이터 분석 가능 조건 파악.
# 마찬가지로 VF별 양품/불량 개수가 존재하는지 확인.
# VF별 양품/불량 개수가 2개 이상이어야 함.
# VF별 양품/불량별 요인 개수가 1개 이하인 것 확인
import pandas as pd
import numpy as np


def df2_isin_df1(df1, df2, group_var):
    """
        두 개의 dataFrame 이 있을 때,(df1, df2)
        df2[group_var] 에 존재하는 모든 CASE 의 df1[group_var] s를 slicing 하는 예제
    :param df1: df2[group_var] 에 존재하는 row 를 slicing 하기 위한 dataFrame
    :param df2: df1 을 slicing 하기위한 dataFrame
    :param group_var:
    :return:
        slicing 한 df1 dataFrame
    """
    result_df = df1.loc[np.all(np.isin(list(df1[group_var].itertuples(index=False, name=None)),
                                       list(df2[group_var].itertuples(index=False, name=None))),
                               axis=1), :]
    return result_df


pd.set_option("display.max_columns", 100)

df = pd.read_csv("test_data/retail-data/all/online-retail-dataset.csv")
df["ctq_result"] =[np.random.randint(0, 2) for _ in range(len(df))]
fac_var = "ctq_result"
ctq_var = "ctq_id"
vf_var = "vf_id"
value_n_var = "value_n"
value_c_var = "value_c"

df.rename({"CustomerID": "ctq_id",
           "StockCode": "value_c",
           "Country": "vf_id",
           "UnitPrice": "value_n"}, axis=1, inplace=True)


class posCheckAnalysis:
    def __init__(self, df: pd.DataFrame, fac_var: str, ctq_var: str, vf_var: str,
                 value_n_var: str = "value_n", value_c_var: str = "value_c"):
        self.df = df
        self.fac_var = fac_var
        self.ctq_var = ctq_var
        self.vf_var = vf_var
        self.value_n_var = value_n_var
        self.value_c_var = value_c_var

    def filter_c_is_analysis_data(self):
        df = self.filter_good_and_bad_ctq_data()
        df = self.filter_good_and_bad_vf_data(df)
        df = self.filter_c_ctq_vf_factor_under_one(df)
        return df

    def filter_n_is_analysis_data(self):
        df = self.filter_good_and_bad_ctq_data()
        df = self.filter_good_and_bad_vf_data(df)
        df = self.filter_n_ctq_vf_std_value_is_zero(df)
        return df

    def filter_good_and_bad_ctq_data(self):
        """
            마찬가지로 CTQ 별(ctq_var) 양품/불량 개수(fac_var)가 2개 이상 존재하는지 확인.
        :param df:
        :return:
        """
        grouped_ctq_vf_fac_df = df.groupby([ctq_var, fac_var])[fac_var].agg(["count"]).reset_index()
        return df.loc[~np.in1d(df[ctq_var], grouped_ctq_vf_fac_df[grouped_ctq_vf_fac_df["count"] < 2][ctq_var]), :]

    def filter_good_and_bad_vf_data(self, df: pd.DataFrame):
        """
            ctq-vf data 내 불량/양품 데이터가 모두 존재하는 데이터만 filtering
        :param df:
        :return:
        """
        grouped_ctq_and_fac_df = df.loc[1:1000, ].groupby([ctq_var,
                                                           vf_var,
                                                           fac_var])[vf_var].agg(["count"]).reset_index()

        if np.all(grouped_ctq_and_fac_df["count"] >= 2):
            return df

        distinct_ctq_and_vf_df = grouped_ctq_and_fac_df.loc[~grouped_ctq_and_fac_df["count"] < 2, :][[ctq_var,
                                                                                                     vf_var]].drop_duplicates()
        result_df = df2_isin_df1(df, distinct_ctq_and_vf_df, [ctq_var, vf_var])
        return result_df

    def filter_n_ctq_vf_std_value_is_zero(self, df: pd.DataFrame):
        """
        vf value 의 표준편차 값이 0이 아닌 데이터만 filtering
        :param df:
        :return:

        """
        grouped_ctq_vf_fac_std_df = df.groupby([ctq_var,
                                                vf_var,
                                                fac_var])[value_n_var].agg(["std"]).reset_index()

        std_is_zero_or_nan = np.logical_or(grouped_ctq_vf_fac_std_df["std"] == 0,
                                           grouped_ctq_vf_fac_std_df["std"] == np.nan)

        if np.all(~std_is_zero_or_nan):
            return df

        result_df = df2_isin_df1(df,
                                 grouped_ctq_vf_fac_std_df.loc[~std_is_zero_or_nan].drop_duplicates([ctq_var, vf_var]),
                                 [ctq_var, vf_var])

        return result_df

    def filter_c_ctq_vf_factor_under_one(self, df: pd.DataFrame):

        grouped_factor_count_df = df.groupby([ctq_var,
                                              vf_var,
                                              fac_var,
                                              value_c_var])[value_c_var].agg("count").reset_index()

        count_is_zero_or_nan = np.logical_or(grouped_factor_count_df["count"] == 0,
                                             grouped_factor_count_df["count"] == np.nan)

        if np.all(~count_is_zero_or_nan):
            return df

        result_df = df2_isin_df1(df,
                                 grouped_factor_count_df.loc[~count_is_zero_or_nan].drop_duplicates([ctq_var, vf_var]),
                                 [ctq_var, vf_var])

        return result_df











        





















