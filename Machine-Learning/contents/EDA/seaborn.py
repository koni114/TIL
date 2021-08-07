#- seaborn에 있는 여러가지 plot 사용
import pandas as pd
import seaborn as sns
df = pd.read_csv('./heart_failure_clinical_records_dataset.csv')

sns.histplot(x='age', data=df, hue='DEATH_EVENT', kde=True)
sns.histplot(data=df.loc[df['creatinine_phosphokinase'] < 3000, 'creatinine_phosphokinase'])
sns.histplot(x='ejection_fraction', data=df, bins=13, hue='DEATH_EVENT', kde=True)

sns.jointplot(x='platelets', y='creatinine_phosphokinase', hue='DEATH_EVENT', data=df, alpha=0.3)
sns.boxplot(x='DEATH_EVENT', y='ejection_fraction', data=df)

