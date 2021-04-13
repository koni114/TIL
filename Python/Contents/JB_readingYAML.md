## python에서 YAML file 읽기
- pyyaml 설치
~~~
pip install pyyaml
~~~
- 두 가지 종류의 yaml file 
~~~
# fruits.yaml file
apples: 20
mangoes: 2
bananas: 3
grapes: 100
pineapples: 1
~~~
~~~
# categories.yaml file
sports:

  - soccer
  - football
  - basketball
  - cricket
  - hockey
  - table tennis

countries:

  - Pakistan
  - USA
  - India
  - China
  - Germany
  - France
  - Spain
~~~
~~~
# process_yaml.py file

import yaml

with open(r'E:\data\fruits.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    fruits_list = yaml.load(file, Loader=yaml.FullLoader)
    print(fruits_list)
~~~

def set_crawling_option : 초기 드라이버 설정
def search_