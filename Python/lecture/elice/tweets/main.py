from tweets_data import trump_tweets
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from wordcloud import WordCloud
from collections import Counter
from string import punctuation

#- 데이터 전처리 실행
def preprocess_text(text):
    text = text.lower()
    symbols = punctuation.replace("@", '').replace('#', '')

    for symbol in symbols:
        text = text.replace(symbol, '')

    words = text.split()
    return words

# 해시태그와 키워드 추출
def analyze_text(words):
    keywords, hashtags, mentions = [], [], []
    filter_words = ['the', 'to', 'of', 'in', 'for', 'and',
                    'from', 'is', 'on', 'it', 'this', 'that',
                    'are', 'was', 'will', 'with', 'very', 'a',
                    'be', 'by', 'must', 'just', 'not']

    for word in words:
        if word in filter_words:
            continue

        if word.startwiths("#"):
            plain_word = word[1:]
            keywords.append(plain_word)
            hashtags.append(plain_word)

        elif word.startwiths("@"):
            plain_word = word[1:]

            keywords.append(plain_word)
            mentions.append(plain_word)

        else:
            keywords.append(word)

        return keywords, hashtags, mentions

def filter_by_month(tweet_data, month):
    month_string = '0' + str(month) if month < 10 else str(month)

    filtered_tweets = []
    for date, tweet in tweet_data:
        if date.startswith(month_string):
            filtered_tweets.append(tweet)

    return filtered_tweets

#- 트윗 통계를 출력
def show_stats():
    keyword_counter = Counter()
    hashtag_counter = Counter()
    mention_counter = Counter()

    for _, tweet in tweets.trump_tweets:
        keyword, hashtag, mention = analyze_text(preprocess_text(tweet))
        keyword_counter += Counter(keyword)
        hashtag_counter += Counter(hashtag)
        mention_counter += Counter(mention)

    top_ten = hashtag_counter.most_common(10)
    for hashtag, freq in top_ten:
        print(f'{hashtag} : {freq}회')


#- 월 별 트윗 개수를 보여주는 그래프 출력
def show_tweets_by_month():
    months = range(1, 13)
    num_tweets = [len(filter_by_month(tweets.trump_tweets, month)) for month in months]
    plt.bar(months, num_tweets, align='center')
    plt.xticks(months, months)
    plt.savefig('graph.png')


def create_word_cloud():

    counter = Counter()
    for _, tweet in tweets.trump_tweets:
        keywords, _, _ = analyze_text(preprocess_text(tweet))
        counter += Counter(keywords)

    trump_mask = np.array(Image.open('trump.png'))
    cloud = WordCloud(background_color='white', mask=trump_mask)
    cloud.fit_words(counter)
    cloud.to_file('cloud.png')

def main(code=1):
    if code == 1:
        show_stats()
    elif code == 2:
        show_tweets_by_month()
    elif code == 3:
        create_word_cloud()


if __name__ == '__main__':
    main(1)


from math import log, e
log(10, e)
log