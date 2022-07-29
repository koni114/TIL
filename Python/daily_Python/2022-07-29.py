import pandas as pd
import seaborn as sns
import os

# 정적 밀도 함수
test_df = pd.read_csv("./test_data/iris.csv")
test_df = test_df.loc[test_df["variety"] != "Setosa", :]
import pandas as pd
import seaborn as sns
import os

# 정적 밀도 함수
test_df = pd.read_csv("./test_data/iris.csv")
test_df = test_df.loc[test_df["variety"] != "Setosa", :]

color_hex = ["#2D9E71", "#663D80"]

sns.distplot(test_df["sepal.length"], hist=False, kde=True, kde_kws={'linewidth': 3})

sns.displot(data=test_df,
            x='sepal.length',
            hue='variety',
            kind='kde',
            fill=True,
            palette=color_hex,
            height=5, aspect=1.5)
color_hex = ["#2D9E71", "#663D80"]

sns.distplot(test_df["sepal.length"], hist=False, kde=True, kde_kws={'linewidth': 3})

sns.displot(data=test_df,
            x='sepal.length',
            hue='variety',
            kind='kde',
            fill=True,
            palette=color_hex,
            height=5, aspect=1.5)

# 동적 밀도 함수(plotly)
import plotly.figure_factory as ff
import numpy as np

x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']
colors = ['#A56CC1', '#A6ACEC', '#63F5EF']

# Create distplot with curve_type set to 'normal'
fig = ff.create_distplot(hist_data, group_labels, colors=colors,
                         bin_size=.2, show_rug=False)

# Add title
fig.update_layout(title_text='Hist and Curve Plot')
fig.show()

import plotly.io as pio

pio.renderers.default = "browser"
import plotly.figure_factory as ff
import numpy as np

x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']
colors = ['#A56CC1', '#A6ACEC', '#63F5EF']

# Create distplot with curve_type set to 'normal'
fig = ff.create_distplot(hist_data, group_labels, colors=colors, curve_type="kde",
                         bin_size=.2, show_hist=False, show_rug=False)

# Add title
fig.update_layout(title_text='Hist and Curve Plot')
fig.show()
