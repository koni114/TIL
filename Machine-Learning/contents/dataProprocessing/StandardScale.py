from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv('./heart_failure_clinical_records_dataset.csv')

X_num = df[['age', 'creatinine_phosphokinase','ejection_fraction', 'platelets','serum_creatinine', 'serum_sodium']]
X_cat = df[['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']]
y = df['DEATH_EVENT']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_num)
X_scaled = pd.DataFrame(X_scaled, columns=X_num.columns)
X = pd.concat([X_scaled, X_cat], axis=1)

