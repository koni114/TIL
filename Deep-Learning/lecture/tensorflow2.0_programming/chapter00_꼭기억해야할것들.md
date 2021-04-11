# tensorflow2.0 꼭 기억해야 할 것들 
- `plt.imshow()` : 이미지 시각화 함수
- `np.reshape()` : 배열의 차원을 변경해주는 함수. 이 때 -1은 차원을 변경한 후 나머지 값을 자동으로 배열한다는 의미
- `np.tile(A, reps)` reps 크기 만큼 반복한 A을 생성해냄
- `np.random.randint(0, 100, 10)` 0 ~ 100중 10개 random sampling
- `np.random.choice(replace = False)` : 중복되지 않는 숫자 random sampling 가능 
- `glob` : 파일들의 리스트를 뽑을 때 사용. 파일의 경로명을 이용해서 원하는 text를 뽑아낼 수 있음
~~~python
from glob import glob
glob("*.exe") # 해당 format에 일치하는 문자 return
glob("*.txt")
glob("/content/sample_data/*.csv")
~~~
- `np.argsort()` : 값 대신 인덱스를 정렬함
- `np.sort()` : 값을 정렬함
