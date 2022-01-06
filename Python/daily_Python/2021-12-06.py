from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd
import joblib
import os

# variable setting
df = pd.DataFrame([['Male', 1], ['Female', 3], ['Female', 2]],
                  columns=['sex', 'age'])
x_var = ['sex']
enc_dir = './pre'
model_name = None
column_drop = True

x_var = [value for value in x_var if value in list(df.columns)]
one_hot_labels = []
if len(x_var) < 1:
    print(f"x_var 가 df 컬럼에 없습니다. = {x_var}")

if enc_dir is None:
    enc_dir = './pre'

if model_name is None:
    model_name = 'enc_fit'

df = df.reset_index()

for var in x_var:

    lnc = LabelEncoder()
    lnc_fit = lnc.fit(df[var])
    df[var] = lnc_fit.transform(df[var])
    joblib.dump(lnc_fit, os.path.join(enc_dir, model_name + '_lnc.pkl'))

    one_hot_label = [var + '_' + label for label in lnc.classes_.tolist()]
    one_hot_labels.extend(one_hot_label)

    enc = OneHotEncoder()
    enc_fit = enc.fit(df[[var]])
    joblib.dump(enc_fit, os.path.join(enc_dir, model_name + '_enc.pkl'))

    enc_transform_array = enc_fit.transform(df[[var]]).toarray()
    df = pd.concat([df, pd.DataFrame(enc_transform_array, columns=one_hot_label)], axis=1)

    if column_drop:
        df.drop(var, axis=1)











