import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
os.getcwd()

font = fm.FontProperties(fname='./elice/font/NanumBarunGothic.ttf')
data = csv.reader(open('./elice/data/subway_2016.csv', 'r'), delimiter=",")

num_passenger1 = []
num_passenger2 = []
station1 = '신림'
line1 = '2호선'
station2 = '강남'
line2 = '2호선'

for row in data:
    if row[1] == station1 and row[0] == line1:
        num_passenger1 = row[2:]
    if row[1] == station2 and row[0] == line2:
        num_passenger2 = row[2:]

trump_tweets = [
    'Will be leaving Florida for Washington (D.C.) today at 4:00 P.M. Much work to be done, but it will be a great New Year!',
    'Companies are giving big bonuses to their workers because of the Tax Cut Bill. Really great!',
    'MAKE AMERICA GREAT AGAIN!'
]


def date_tweet(tweet):
    for index in range(len(tweet)):
        print('2018년 1월' + str(index+1) + '일: ' + tweet[index])


trump_tweets = ['thank', 'you', 'to', 'president', 'moon', 'of', 'south', 'korea', 'for', 'the', 'beautiful',
                'welcoming', 'ceremony', 'it', 'will', 'always', 'be', 'remembered']


def preprocessing_tweets(tweet):
    for text in tweet:
        if text.startswith('k'):
            print(text)

preprocessing_tweets(trump_tweets)

#- 문장을 단어 단위로 구분하기
trump_tweets = "thank you to president moon of south korea for the beautiful welcoming ceremony it will always be remembered"

def break_into_words(text):
    return trump_tweets.split(" ")


#- b로 시작하는 요소들을 new_list에 추가
trump_tweets = ['america', 'is', 'back', 'and', 'we', 'are',
                'coming', 'back', 'bigger', 'and', 'better',
                'and', 'stronger', 'than', 'ever', 'before']

def make_new_list(text):
    new_list = []
    for word in text:
        if word.startswith("b"):
            new_list.append(word)

    return new_list


word = '!'
word.replace("!", ".")
word.re

'/* elice */'.replace('/', '').replace('*', '').replace(' ', '')
