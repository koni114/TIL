import pandas as pd
import numpy as np

# 다음의 데이터를 활용하여 연속형 변수 C1 을 이산형화 시켜보세요
# - C1 컬럼의 데이터를 10개의 구간으로 나누고, 이를 (1 ~ 10) 까지로 만들어본 후, C1_bin 컬럼에 넣어 보세요.
# - 만든 C1_bin 컬럼 값을 다시 one-hot encoding 을 수행해보세요
# - 이 때, 첫 번째 변수를 삭제해보세요

from sklearn.preprocessing import MinMaxScaler

np.random.seed(10)
df = pd.DataFrame({'C1': np.random.randn(20),
                   'C2': ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
                          'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']})

np_lin = np.linspace(np.min(df["C1"]), np.max(df["C1"]), 10)
df["C1_bin"] = np.digitize(df["C1"], np_lin)

pd.get_dummies(df["C1_bin"], prefix="x", drop_first=True)

