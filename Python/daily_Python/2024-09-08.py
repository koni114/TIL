import pandas as pd
import numpy as np

# 정답이 포함되어 있는 DataFrame.
# COL: single_question, len, language, single_question_keyword 
gts_df = pd.DataFrame({'single_question': [[['골프, 치킨에 관심이 있는 사용자 알려줘'],
                                            ['아이스 아메리카노를 검색한 사용자 알려줘'],
                                            ['삼성전자에 관심이 있는 사용자 알려줘']
                                            ]],
                       'len': [3],
                       'language': ['ko'],
                       'single_question_keyword': [[['골프', '치킨', '관심', '사용자'],
                                                    ['아이스', '아메리카노', '검색', '사용자'],
                                                    ['삼성전자', '관심', '사용자']]]})
# LLM 예측 결과 DataFrame.
# COL: llm_len, llm_single_question_keyword 
preds_df = pd.DataFrame({'llm_len': [2],
                         'llm_single_question_keyword': [[['골프', '치킨', '관심', '사용자'],
                                                          ['아이스 아메리카노', '검색']
                                                          ]]})

result = pd.DataFrame()
 
# single question 의 len 의 Metric 지표값 계산.
result['count_accuracy'] = (1 - round(abs(preds_df['llm_len'] - gts_df['len'])/ gts_df['len'], 
                                      4)).apply(lambda x: max(x, 0))

# language 가 영문인 경우, 전체 문장을 소문자로 변환.
# single_question_keyword -> 3차원 matrix
gts_df.loc[gts_df['language'] == 'en', 'single_question_keyword'] = \
    gts_df.loc[gts_df['language'] == 'en','single_question_keyword'].apply( lambda x: 
            [[item.lower() for item in items ] for items in x ]
        )

# 성능 평가
list1 = gts_df.loc[0, 'single_question_keyword']
list2 = preds_df.loc[0, 'llm_single_question_keyword']
language = gts_df.loc[0, 'language']

# 리스트 안의 서브 리스트끼리 similarity matrix 계산하는 함수
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

list1_texts = [' '.join(sublist) for sublist in list1 ]
list2_texts = [' '.join(sublist) for sublist in list2 ]

# combine all lists for vectorization
combined_list = list1_texts + list2_texts
tfidfv = vectorizer.fit(combined_list)

# vector vocabulary
print(tfidfv.vocabulary_)

vectors = tfidfv.transform(combined_list)

# Split vectors back into list1 and list2
vectors1 = vectors[: len(list1_texts) ]
vectors2 = vectors[len(list1_texts):  ]

print(vectors1.toarray()) # 정답지 -> 3 x 8(single_question 3개)
print(vectors2.toarray()) # 예측  ->  2 x 8(single question 2개)

# Compute similiarity matrix
from sklearn.metrics.pairwise import cosine_similarity

# 3 x 2 matrix 의 Cosine similarity 값 계산됨.
similarity_matrix = cosine_similarity(vectors1, vectors2)

from scipy.optimize import linear_sum_assignment

# Hungarian Method 를 활용한 최적화된 조합값 계산
# - 를 붙이는 이유는 조합의 결과가 가장 작은 값으로 계산해주기 때문(목적함수 값이 MIN.)
row_ind, col_ind = linear_sum_assignment(-similarity_matrix)

# 만약 정답지와 예측지와 single_question 의 개수가 다른 경우, np.NaN 으로 반환되게 하기 위함.
def exception(i, col_ind):
    '''예외처리 함수'''
    try:        
        return (i, col_ind[i])
    except:
        return (i, np.NaN)

# matches : [(0, 0), (1, 1), (2, nan)]
matches = [exception(i, col_ind) for i in range(len(list1))]

matching = {}
# indx, value =  list(enumerate(matches))[0]
for indx, value in enumerate(matches):
    # matching sentence 가 없는 경우, -> 모든 값을 0으로 처리.
    if np.isnan(value[1]):
        matching[indx] = [0, 0, 0, 0]
        continue
    
    # 전처리를 위해 string 으로 변환
    gts = list1[value[0]]
    preds = list2[value[1]]
    
    if language == 'en':
        from textblob import TextBlob
        
        # 전처리를 위해 string 으로 변환
        gts = ','.join(gts)
        preds = ','.join(preds)
        
        # keyword 의 공백 제거
        gts = gts.replace(" ", "")
        
        # 복수형 -> 단수형 치환
        gts = TextBlob(gts).words.singularize()
        preds = TextBlob(preds).words.singularize()
            
    tp, tn, fp, fn = [0, 0, 0, 0]
    
    for keyword in preds:
        if keyword in gts:
            tp += 1
        else:
            fp += 1
    
    for keyword in gts:
        if keyword not in preds:
            fn += 1
    
    # calculate accuracy score       
    if tp+fp+fn+tn == 0:
        accuracy_score = 1
    else:
        accuracy_score = round((tp+tn) / (tp+fp+fn+tn), 4)

    # calculate recall score               
    if tp+fn == 0:
        recall_score = 1
    else:
        recall_score = round(tp / (tp+fn), 4)
    
    # calculate precision score               
    if tp+fp == 0:
        precision_score = 1
    else:
        precision_score = round(tp / (tp+fp), 4)
    
    # calculate f1 score               
    if precision_score == 0 and recall_score == 0:
        f1_score = 0
    else:
        f1_score = round(
            (2 * precision_score * recall_score) / (precision_score + recall_score), 4
        )
    
    matching[indx] = [accuracy_score, recall_score, precision_score, f1_score]

    # 각 리스트의 길이 확인
    num_elements = len(next(iter(matching.values())))
    
    # 결과를 저장할 리스트
    results = []
    
    # 각 항목끼리 기하평균 계산 
    # i = 0
    for i in range(num_elements):
        # 해당 인덱스들의 값을 모음
        values = [lst[i] for lst in matching.values()]
        geom_mean = np.exp(np.mean(np.log(values))) # 기하 평균
        results.append(geom_mean)
    
    print("geo_mean", results)
    
    
    