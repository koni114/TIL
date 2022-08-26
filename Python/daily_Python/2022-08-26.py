# Connecting Matplotlib with plotly
# RivVgfm9UXJpczbbV3Xe

import matplotlib.pyplot as plt
import plotly.io as pio
import seaborn as sns
import pandas as pd
import chart_studio
import kaleido
import os
os.getcwd()

fig = plt.figure()

# 정적 밀도 함수
test_df = pd.read_csv("/Users/heojaehun/gitRepo/TIL/Python/daily_Python/test_data/iris.csv")
test_df = test_df.loc[test_df["variety"] != "Setosa", :]

color_hex = ["#2D9E71", "#663D80"]

sns.displot(data=test_df,
                      x='sepal.length',
                      hue='variety',
                      kind='kde',
                      fill=True,
                      palette=color_hex,
                      height=5, aspect=1.5)

plt.show()


pio.write_image(mpl_fig, "test.png")


chart_studio.tools.set_credentials_file(username='swallow9212', api_key='RivVgfm9UXJpczbbV3Xe')
unique_url = chart_studio.plotly.plot_mpl(mpl_fig, filename="test plot")

