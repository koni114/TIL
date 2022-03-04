# 동일 길이로 나누어서 범주 나누기: pd.cut()
# 동일 개수로 나누어서 범주 만들기: pd.qcut()

import numpy as np
import pandas as pd
np.random.seed(123)
df = pd.DataFrame({'col_1': np.random.randint(20, size=20),
                   'col_2': np.random.randn(20)})

df_col_1_factor = pd.cut(df.col_1, 4)

df_grouped = df.col_1.groupby(df_col_1_factor)
df_grouped.agg(['count', 'mean', 'std', 'min', 'max'])

def summary_func(grp):
    return {'count': grp.count(),
            'std': grp.mean(),
            'mean': grp.mean(),
            'min': grp.min(),
            'max': grp.max()}

df_grouped.apply(summary_func).unstack()
df_grouped.apply(summary_func)

# labels = np.arange(4, 0, -1) 로 지정하면 거꾸로 지정됨
bucket_qcut_label_col_2 = pd.qcut(df.col_2, 4, labels=np.arange(4, 0, -1))

# [4 < 3 < 2 < 1] 순서로 동일 개수로 나눈 4개의 그룹별 통계량
grouped = df.col_2.groupby(bucket_qcut_label_col_2)
grouped.apply(summary_func).unstack()

# 그룹 별