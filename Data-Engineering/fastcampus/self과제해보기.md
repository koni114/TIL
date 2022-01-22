## self 과제 해보기
### spark 를 활용한 과제
1. `restaurant_reviews.csv` 를 활용하여 카테코리(중식, 분식, 일식, 아시안, 패스트푸드) 별 가격 평균을 spark code 로 작성하여 만들어보세요. 다음과 같은 제약 조건을 만족해야 합니다.
  - Spark UI 에서 `category-review-average` 로 검색이 가능해야 합니다.
  - `map`, `mapValues`, `reduceByKey` 를 적절하게 사용하여 속도가 최적화 될 수 있도록 해야합니다.
  - 최종 결과는 `result` 변수에 담아야 하며, `collect` 함수를 통해 출력하세요.