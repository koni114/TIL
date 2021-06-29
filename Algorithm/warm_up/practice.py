import pandas as pd
import numpy as np
stock_series = pd.Series([92300, 94300, 92100, 92400, 92600])
stock_list = np.array([92300, 94300, 92100, 92400, 92600])

#- 시리즈 만들기
list_stock = [92300, 94300, 92100, 92400, 92600]
pd.Series(list_stock)

dict_stock = {'2021-06-28': 92300,
              '2021-06-27': 94300,
              '2021-06-26': 92100,
              '2021-06-25': 92400,
              '2021-06-24': 92600}

stock = pd.Series(dict_stock)
print(stock)


file_path = './test_data/titanic_train.csv'
titanic_train = pd.read_csv(file_path, sep=',')


list_stock = [92300, 94300, 92100, 92400, 92600]
dates = ['2021-06-28', '2021-06-27', '2021-06-26', '2021-06-25', '2021-06-24']
stock = pd.Series(data=list_stock, index=dates)

#- 인덱스 초기화
stock.reset_index(drop=True, inplace=True)
np.sum(titanic_train.isnull())

stock.append(stock, ignore_index=True)
score_math = pd.Series([90, 80, 10, 20], index=['홍길동', '한사랑', '박여인', '일지매'])
score_korean = pd.Series([100, 50, 20], index=['홍길동', '박여인', '일지매'])

dict_test = {
    '이름': ['홍길동', '한사랑', '일지매', '박여인'],
    '등급': ['Gold', 'Bronze', 'Silver', 'Gold'],
    '점수': [56000, 23000, 44000, 52000]
}

df = pd.DataFrame(dict_test)

#- 일반 열을 인덱스로 지정 가능
file_path = './test_data/titanic_train.csv'
titanic_train = pd.read_csv(file_path, sep=',')

titanic_train.set_index(['PassengerId'], inplace=True)
titanic_train.reset_index(inplace=True)

pd.set_option('display.max_row', 100)
pd.set_option('display.max_columns', 100)


def male_or_female(value):
    if value.find('Mr') != -1 or value.find('Mrs') != -1:
        return 'male'
    else:
        return 'female'


sorted(titanic_train['Survived'].unique())
sorted(titanic_train['Pclass'].unique())
sorted(titanic_train['Sex'].unique())
sorted(titanic_train['Parch'].unique())

#- 데이터 조회 - 조건 조회
tic_age = titanic_train['Age']
more_than_50 = titanic_train[tic_age > 50]

#- and, or 조건으로 여러 조건과 함께 조회
is_male = titanic_train['Name'].str.contains('Mr|Mrs')

titanic_train.drop('Cabin', axis=1, inplace=True)
titanic_train.drop(['Cabin', 'Ticket'], axis=1, inplace=True)

pd.concat([titanic_train,
           pd.get_dummies(titanic_train['Sex'])],
          axis=1)

titanic_train.isnull().any()
titanic_train.isnull().sum()

titanic_train['Age'].fillna(round(titanic_train['Age'].mean(), 4), inplace=True)