from bs4 import BeautifulSoup

cs_info_dict = {'name': "허재훈", 
                'query': "query_example_1",
                'emailDateAt': "2024년 10월 1일",
                'destructedAt': "2024년 10월 1일"}

# 파일에서 HTML 내용을 읽어옵니다.
with open('test.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# BeautifulSoup을 사용하여 HTML을 파싱합니다.
soup = BeautifulSoup(html_content, 'html.parser')

# 1. class='user'인 "사용자" 텍스트를 "허재훈"으로 변경합니다.
span_user = soup.find('span', class_='user')
if span_user:
    span_user.string = '허재훈'

# 2. class='day'인 "2024년 09월 25일" 텍스트를 "2024년 10월 1일"로 변경합니다.
span_day = soup.find('span', class_='day')
if span_day:
    span_day.string = '2024년 10월 1일'

# 3. <tbody><tr><td> 태그 내의 "김삼성"을 "허재훈"으로 변경합니다.
tbody = soup.find('tbody')
if tbody:
    td_tags = tbody.find_all('td')
    for td in td_tags:
        if td.string and cs_info_dict.get(td.string):
            td.string = td.string.replace(td.string, 
                                          cs_info_dict.get(td.string))

# 4. 새로운 <tr>을 생성하여 <th>와 <td>를 추가합니다.
if tbody:
    # 새로운 <tr> 태그 생성
    new_tr = soup.new_tag('tr')
    
    # <th> 태그 생성 및 내용 추가
    new_th = soup.new_tag('th')
    new_th.string = 'operator'
    new_tr.append(new_th)
    
    # <td> 태그 생성 및 내용 추가
    new_td = soup.new_tag('td')
    new_td.string = 'Union'
    new_tr.append(new_td)
    
    # <tbody>에 새로운 <tr> 추가
    tbody.append(new_tr)

# 변경된 HTML을 새로운 파일에 저장합니다.
with open('modify_text.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))