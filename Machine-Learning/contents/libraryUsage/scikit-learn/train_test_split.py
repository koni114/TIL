from sklearn.model_selection import train_test_split
import pandas as pd
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

y = df['DEATH_EVENT']
X = df[[col for col in df.columns if col != 'DEATH_EVENT']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print(f"X_train shape : ", X_train.shape)
print(f"X_test shape : ", X_test.shape)
print(f"y_train shape : ", y_train.shape)
print(f"y_test shape : ", y_test.shape)

