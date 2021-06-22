#- 키워드 확인
import keyword
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


print(keyword.kwlist)
##############
#### 문자열 ####

#- 문자열 특성을 파악하는 메소드
#- isalnum : 모든 문자가 알파벳이나 숫자면 True 반환
text = 'company12'
text.isalnum()      #- 모든 문자가 알파벳과 숫자로 이루어져 있기 때문에 True 반환

#- isalpha : 모든 문자가 알파벳이면 True 반환
only_alpha = 'abcde'
text.isalpha()  #- True

not_only_alpha = 'company12'
not_only_alpha.isalpha()     #- False

#- isdecimal : 모든 문자가 0~9이면 True 반환
#- isdigit : 모든 문자가 숫자 모양이면 True 반환, 3^2의 제곱근도 포함
"32".isdigit()

#- isidentifier : 모든 문자가 식별자면 True 반환
#- ** 식별자란 변수, 함수, 클래스, 모듈, 기타 객체를 식별하는데 사용되는 이름 --> 쉽게 말하면 변수!
#-    예를 들어 !, *, &는 식별자로 사용될 수 없음
A = 'hello_world'
"A".isidentifier()  #- True
"*".isidentifier()  #- False

#- islower: 모든 문자가 소문자면 True 반환
#- isnumeric: 모든 문자가 숫자이면 True 반환, 1/2도 포함
#- isprintable: 모든 문자가 print 가능한 문자면 True 반환, \n은 print 가 불가한 문자
#- isspace : 모든 문자가 공백이면, True 반환
#- istitle: 모든 단어의 첫 글자가 대문자이면 True 반환
#- isupper: 모든 문자가 대문자이면 True 반환

##############
#### 리스트 ####

#- del 문으로 요소 하나 지우기
nums = list(range(10, 100, 10))
print(nums)
del nums[7]
print(nums)

#- 범위로 여러 요소 지우기, 모두 지우기
nums[4:] = []
print(nums)

#- 리스트 관련 메소드
#- append, count, del, extend, insert, remove, reverse, sort

###############
#### 딕셔너리 ####
members = (('홍길동', 100), ('일지매', 90), ('힌여인', 90), ('강우동', 95))
members_dict = dict(members)
print(members_dict)

##################
#### 집합(set) ####
member_set1 = {'홍길동', '한사랑', '일지매', '박여인'}
member_set2 = {'한사랑', '홍길민', '강우동'}

member_set3 = member_set1.intersection(member_set2)     #- 교집합
member_set4 = member_set1 - member_set2                 #- 차집합
member_set5 = member_set1.union(member_set2)            #- 합집합

#- 집합 관련 메소드
#- add : 집합에 원소 하나를 추가
#- clear : 집합에서 모든 원소 제거
#- discard : 집합에서 특정 원소 제거. 지정한 원소를 찾지 못하면 무시
member_set1.discard('홍길동')
print(member_set1)
member_set1.discard('없음')  #- error 발생하지 않음

#- pop : 집합에 무작위로 원소 하나를 제거
#- remove : 집합에서 특정 원소 제거, 지정한 원소를 찾지 못하면 오류 발생
#- update : 집합에 여러 원소(리스트, 튜플, 딕셔너리)를 추가

###########
## Numpy ##
import numpy as np
a = np.array([1, 2, 3, 4, 5])

#- Axis: 배열의 각 축
#- Rank: 축의 개수
#- Shape: 축의 길이

#- [3x4 형태인 배열의 경우]
#- axis 0, axis 1을 갖는 2차원 배열
#- Rank 2 array, 첫 번째의 축의 길이는 3, 두 번째 축의 길이는 4
#- shape 는 (3,4)

#- 1차원 배열
a = np.array([1, 2, 3, 4, 5])
print(a)
print(type(a))
print(a.ndim)   #- 차원
print(a.shape)
print(a.dtype) #- 데이터 형식
print(a[0], a[1], a[2])

#- 2차원 배열
a = np.array([[1.5, 2.5, 3.2], [4.2, 5.7, 6.4]])

print(a)
print(a.ndim)   #- 2
print(a.shape)  #- (2, 3)
print(a.dtype)  #- float64

a = np.array([list('python'), list('flower')])
print(a)

dic = {'a': 1, 'b': 2, 'c': 3}
a = np.array([list(dic.keys()), list(dic.values())])
print(a)

st = {1, 2, 3}
a = np.array([list(st), list(st)])
print(a)

#- reshape --> 기존 배열을 새로운 배열 형태로 구성
a = np.array([[1, 2, 3],
             [4, 5, 6]])

b = np.reshape(a, (6, 1))
print(b)

a.reshape(3, -1)  #- a를 3행으로 된 배열로 변환
a.reshape(-1, 2)  #- a를 2열로 된 배열로 변환

np.zeros((2, 2))          #- 0으로 채워진 배열
np.ones((1, 2))           #- 1로 채워진 배열
np.full((2, 2), 7.)       #- 7로 채워진 배열
np.eye(2)                 #- 정방향 행렬
np.random.random((2, 2))  #- 랜덤 값으로 채운 배열

##- 배열 데이터 조회
#- 팬시 인덱싱
#  - 불리안 방식 배열 인덱싱
#  - 정수 방식 배열 인덱싱
#- 배열 인덱싱과 슬라이싱 정리

#- 1차원 배열
score = np.array([78, 91, 84, 89, 93, 65])
score_more_than_90 = score[score >= 90]
print(score_more_than_90)

#- 2차원 배열
score_2d = np.array([[78, 91, 84, 89, 93, 65],
                     [82, 87, 96, 79, 91, 93]])

var1 = score_2d[0][score_2d[0] >= 90] #- array([91, 93])
var2 = score_2d[1][score_2d[1] >= 90] #- array([96, 91, 93])

#- 정수 방식 배열 인덱싱
a = np.array([[1, 2],
              [3, 4],
              [5, 6]])

b = a[[0, 1, 2]]
print(b)

c = a[[0, 2]]
print(c)

d = a[[0]]
print(d)

f = a[[0, 1, 2], [0, 1, 0]]
g = a[[0, 0], [1, 1]]

#- 4 x 3 형태의 2차원 배열 만들기
a = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]])

b = np.arange(4)
c = np.array([0, 2, 0, 1])
d = a[b, c]                   #- [1, 6, 7, 11]
a[b, c] += 10                 #- 해당 위치의 값에 10씩 더함

#- np.array 배열을 슬라이싱 할 때,
#- 인덱스 번호, 범위, 인덱스와 범위로 가져올 수 있음
a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])

b = a[1, 1]
print(b)     # 6

c = a[[0, 1, 2], [0, 1, 1]]
print(c)

d = a[1:2, :]
print(d)      #- 5,6,7,8

e = a[1, :]
print(e)      #- 5,6,7,8

#- 배열 변환과 연산
# 1- 배열 변환
# 2- 기본 연산(사칙연산)
# 3- 리스트와 다른 점
# 4- 행렬 연산
# 5- Shuffle, Sampling, Split

# 1- 배열 변환
#- 기존 배열의 데이터 형식은 astype 메소드로 변경
a = np.array([1, 2])
print(a.dtype)

a = np.array([1.0, 2.0])
print(a.dtype)

a = np.array([1.9, 8.0], dtype=np.int32)
print(a)

x = np.array([1, 2])
print(type(x))

#- np.array -> tolist
y = x.tolist()
print(y)
print(type(y))

# 3- 리스트와 다른 점
# ** 리스트 사이에서의 연산은 안되는 경우가 많음
height = [1.73, 1.68, 1.71, 1.89, 1.79]
weight = [65.4, 59.2, 63.6, 88.4, 68.7]
weight / height ** 2 #- error 발생!

np_height = np.array(height)
np_weight = np.array(weight)
np_weight / np_height ** 2

#- 동일한 연산자에 대한 작동방식이 다름
python_list = [1, 2, 3]
numpy_array = np.array([1, 2, 3])

python_list + python_list  #- [1, 2, 3, 1, 2, 3]
numpy_array + numpy_array  #- array([2, 4, 6])

#- 행렬 곱
#- np.array 의 dot 함수는 행렬 곱을 나타냄
a = np.array([9, 10])
b = np.array([11, 12])
a.dot(b)  #- 9 * 11 + 10 * 12 = 219

a = np.array([[1, 2], [3, 4]])
b = np.array([9, 10])
a.dot(b)

#- 2차원 배열과 2차원 배열의 행렬 곱
# 4- 행렬 연산
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
a.dot(b)

#- 행렬 합
np.sum(a)
np.sum(a, axis=0)
np.sum(a, axis=1)

#- 전치 행렬
print(a)
print(a.T)

#- Shuffle, Sampling, Split
#- Shuffle: 기존 데이터들 무작위로 섞기
#- Sampling: 임의의 데이터 추출하기(복원, 비복원 추출)
#- split: 데이터 분할하기
data = np.genfromtxt('./test_data/sampledata/chemical.csv')
np.random.shuffle(data)

np.random.choice(data, 4, replace=False)  #- 비복원 랜덤 추출 4개
s1, s2, s3, s4 = data[:5], data[5:10], data[11:15], data[:15]

#####################
## Pandas - Series ##
#####################
# 1- 시리즈 이해
# 2- 시리즈 만들기
# 3- CSV 파일에서 데이터 불러오기
# 4- 인덱스 지정
# 5- 시리즈 인덱싱과 슬라이싱
# 6- 시리즈 연산
# 7- 차트 그리기
import pandas as pd

# 1- 시리즈 이해
# - DataFrame 과 더불어 Pandas 가 제공하는 자료 구조 중 하나
# - 인덱스와 값으로 구성되어 키와 값으로 구성되는 딕셔너리와 유사
# - 객체 정보, 일부 데이터, 집계 결과가 시리즈로 저장되는 경우가 많음
stock_series = pd.Series([92300, 94300, 92100, 92400, 92600])
stock_numpy = np.array([92300, 94300, 92100, 92400, 92600])
stock_list = [92300, 94300, 92100, 92400, 92600]
print(stock_series[1:])
print(stock_numpy[1:])
print(stock_list[1:])

# 2- 시리즈 만들기
list_stock = [92300, 94300, 92100, 92400, 92600]
stock = pd.Series(list_stock)

#- key -> index, value -> value
dict_stock = {'2019-02-15': 92300,
              '2019-02-16': 94300,
              '2019-02-17': 92100,
              '2019-02-18': 92400,
              '2019-02-19': 92600}
stock = pd.Series(dict_stock)
print(stock)

# 3- CSV 파일에서 데이터 불러오기
file_path = "./test_data/sampledata/chemical.csv"
df = pd.read_csv(file_path, sep=',')
s = df['V1']
df.head()

# 4- 인덱스 지정
#- 만들 때 인덱스 지정하기
list_stock = [92300, 94300, 92100, 92400, 92600]
dates = ['2019-02-15', '2019-02-16', '2019-02-17',
         '2019-02-18', '2019-02-19']
stock = pd.Series(list_stock, index=dates)

#- 기존 인덱스 변경하기
stock = pd.Series([92300, 94300, 92100, 92400, 92600])
stock.index = dates

#- 인덱스 초기화
stock.reset_index(drop=True, inplace=True)

#- 시리즈 정보 확인
print(stock.index)
print(stock.values)
print(stock.dtype)
print(stock.shape)

#- NaN 값(=결측치) 확인
#- NaN 값은 isnull(), notnull()을 통해 처리
sum(df['V1'].isnull())

# 5- 시리즈 인덱싱과 슬라이싱
print(stock.iloc[3])
print(stock.loc['2019-02-15'])

print(stock.iloc[[0, 2]])
print(stock.loc[['2019-02-15', '2019-02-16']])

# 5- 시리즈 인덱싱과 슬라이싱
print(stock.iloc[0:3])
print(stock.loc['2019-02-15':'2019-02-17'])

#- 시리즈 결합
#- append 함수를 사용해 시리즈를 결합할 수 있음
#- ignore_index = True 를 지정하면 위치에 따른 정수 인덱스 초기화
print(stock.append(stock, ignore_index=True))

# 6- 시리즈 연산
#- 인덱스 위치가 달라도 인덱스의 값을 기준으로 연산 수행
score_math1 = pd.Series([90, 80, 10, 20], index=['홍길동', '한사랑',
                                                 '일지매', '박여인'])
score_math2 = pd.Series([90, 80, 10], index=['홍길동', '일지매', '한사랑'])

print(score_math1 + score_math2)

########################
## Pandas - DataFrame ##
########################
# 1- 데이터프레임 만들기
# 2- CSV 파일에서 데이터 불러오기
# 3- 데이터 살펴보기
# 4- 데이터 조회
# 5- 데이터프레임 변경
# 6- GroupBy, Join, Rolling & Shift
# 7- NaN 값 처리

# 1- 데이터프레임 만들기
#- 다음 세 가지를 우선 지정해야 함
#  --> 데이터, 인덱스, 열 이름
#  --> 인덱스, 열 이름을 지정하지 않으면 위치에 기반한 정수가 설정됨
#  --> 의미 있는 값(날짜가 대표적임)이 인덱스가 되면 분석이 용이

#- dataFrame 만들기
#- 딕셔너리에서 만들면, key 가 열이 됨
dict = {
    '이름': ['홍길동', '한사랑', '일지매', '박여인'],
    '등급': ['Gold', 'Bronze', 'Silver', 'Gold'],
    '점수': [56000, 23000, 44000, 52000]
}
df = pd.DataFrame(dict)
df.head()

#- 리스트에서 만들 때는, 인덱스와 열 이름을 지정
lst = [['홍길동', 'Gold', 56000],
       ['한사람', 'Bronze', 23000],
       ['일지매', 'Sliver', 44000],
       ['박여인', 'Gold', 52000]]

df = pd.DataFrame(lst,
                  index=[1, 2, 3, 4],
                  columns=['이름', '등급', '점수'])
df.head()

#- 일반 열을 인덱스로 지정할 수 있음
df.set_index(['이름'], inplace=True)
df.head()

# 2- CSV 파일에서 데이터 불러오기
#- 많은 데이터를 갖는 데이터프레임을 만들 때는 일반적으로
#  - DB에 연결해 직접 가져오거나,
#  - CSV 파일을 읽어서 데이터를 가져옴

#- Github 에서 CSV 파일을 읽어오는 예
f_path = 'https://gist.githubusercontent.com/michhar/2dfd2de0d4f8727f873422c5d959fff5/raw/fa71405126017e6a37bea592440b4bee94bf7b9e/titanic.csv'
df = pd.read_csv(f_path, sep=',', skipinitialspace=True)
df.head()

#- 파일 읽기: pd.read_csv(), pd.read_excel()
#- 파일 쓰기: pd.to_csv(), pd.to_excel()
df.columns
df.set_index(['PassengerId'], inplace=True)
df.head()

df.reset_index(inplace=True)
df.head()

# 3- 데이터 살펴보기
df.head()
df.tail(3)

#- 더 많은 행과 열을 출력하고 싶을 때, option 변경
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

#- 기초 통계량 살펴보기
df.describe()

#- 데이터 살펴 보기 - 정렬
#- 인덱스로 정렬   --> axis = 0
#- 열 이름으로 정렬 --> axis = 1
#- 열 값으로 정렬  --> by = ['name1', 'name2']
df.sort_index(axis=0, ascending=False).head()
df.sort_index(axis=1, ascending=False).head()
df.sort_values(by=['Age', 'Fare'], ascending=[False, True]).head()

# 4.1 데이터 조회 - 열 조회
#- df['열이름']   --> Series
#- df[['열이름']] --> DataFrame
df['Age'].head()
df[['Age']].head()

#- 중복제거 --> unique()
df['Embarked'].unique()

#- 세 개의 열을 동시에 조회
df[['Age', 'Embarked', 'Fare']].head()

# 4.2 데이터 조회 - 행 조회
#- iloc --> 정수형 위치 인덱스, 0부터 시작하는 인덱스로 조회
#- loc  --> 인덱스 이름으로 조회
print(df.iloc[[0]])         #- 0행 조회
print(df.iloc[[1, 3, 6]])   #- 1, 3, 6행 조회
print(df.iloc[1:4])         #- 1~3행 조회

print(df.loc[[1]])
print(df.loc[[2, 3]])
print(df.loc[[2, 5, 7]])

# 4.3 데이터 조회 - 일부 행, 열 조회
print(df.iloc[1, 1])
print(df.iloc[0:4, 0:3])

print(df.loc[1:4, ])
print(df.loc[1:4, ['Age', 'Embarked', 'Fare']])

# 4.4 데이터 조회 - 조건 조회
df[df['Age'] > 50].shape #- 조건을 비교한 결과 True인 값 조회
df[df['Age'].isin([50, 51])].head()

# and, or 조건으로 여러 조건과 함께 조회
df[(df['Age'] >= 20) & (df['Age'] <= 50)].head()

#- contains --> 문자열에 포함여부 확인
df[df['Embarked'].str.contains('S') & df['Embarked'].notnull()].head()

# 4.5- 데이터 조회 - 샘플링
print(df.sample(5).shape)
print(df.sample(frac=0.2).shape)
print(df.sample(frac=1).shape)


# 5.1- 데이터프레임 변경 - 값 변경
df.loc[1, 'Age'] = 'value_chg'
df.iloc[2, 0] = 'first_class'
df.loc['1번':'3번', ['Age', 'Embarked']] = [np.NaN, 0]
df.loc[df['Age'] >= 50, 'Age'] = '100'

# 5.2- 데이터프레임 변경 - 열 이름 변경
df.rename(columns={"Age": "나이"})

# 5.2- 데이터프레임 변경 - 열 삭제
# - axis=1: 열을 삭제
# - inplace=True: df 에서 직접 삭제
df.drop('Cabin', axis=1, inplace=True)
df.drop(['나이', '등급'], axis=1, inplace=True)

# - get_dummies: 함수 사용
# - 범주형 데이터를 숫자로 변환
df_rank = pd.get_dummies(df['Embarked'])
print(df_rank)

# 5.3- 데이터프레임 변경 - 열 합치기
# axis = 1, --> join:  inner, outer 둘 다 존재
# axis = 0, --> rbind: inner, outer 둘 다 존재

df_new = pd.concat([df, df_rank], axis=1)
df_new.drop('Embarked', axis=1, inplace=True)
print(df_new)

# 6- GroupBy, Join, Rolling & Shift
print(df.groupby(by='Embarked', as_index=False)['Age'].mean())
print(df.groupby(by=['Embarked', 'Sex'], as_index=False)['Age'].mean())
print(df.groupby(by=['Embarked', 'Sex'], as_index=False)['Age'].count())

# 7. join(Merge) 사용
# - 특정 열(key) 기준으로 두 데이터프레임 합치기
# - 공통된 열이 있으면 그 열을 key로 사용
mean_by_embarked = df.groupby(by=['Embarked'], as_index=False)['Age'].mean()
mean_by_embarked.rename(columns={'Age': 'Age_mean'}, inplace=True)

cnt_by_embarked = df.groupby(by=['Embarked'], as_index=False)['Age'].count()
cnt_by_embarked.rename(columns={'Age': 'Age_cnt'}, inplace=True)

pd.merge(mean_by_embarked, cnt_by_embarked)
pd.merge(mean_by_embarked, cnt_by_embarked, on='Embarked', how='left')
