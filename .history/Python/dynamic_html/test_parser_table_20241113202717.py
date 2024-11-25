from bs4 import BeautifulSoup

# 여러 테이블에 대한 데이터 목록
cs_info_list = [
    {
        'name': "허재훈",
        'query': "query_example_1",
        'emailDateAt': "2024년 10월 1일",
        'destructedAt': "2024년 10월 1일"
    },
    {
        'name': "김영희",
        'query': "query_example_2",
        'emailDateAt': "2024년 11월 1일",
        'destructedAt': "2024년 11월 30일"
    },
    {
        'name': "박철수",
        'query': "query_example_3",
        'emailDateAt': "2024년 12월 1일",
        'destructedAt': "2025년 1월 1일"
    }
]

# 파일에서 HTML 내용을 읽어옵니다.
with open('test.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# BeautifulSoup을 사용하여 HTML을 파싱합니다.
soup = BeautifulSoup(html_content, 'html.parser')

# 기존 .breakAgree03 요소를 찾아서 다수의 테이블을 추가합니다.
for idx, cs_info_dict in enumerate(cs_info_list):
    # 새로운 "내용 n" 제목 추가
    break_agree_div = soup.new_tag("div", **{"class": "breakAgree03"})
    span_title = soup.new_tag("span")
    span_title.string = f"내용 {idx + 1}"
    break_agree_div.append(span_title)

    # 새로운 테이블 생성
    new_table = soup.new_tag("table", **{"class": "aTable"})
    colgroup = soup.new_tag("colgroup")
    col1 = soup.new_tag("col", style="width:18%;")
    col2 = soup.new_tag("col", style="width:*;")
    colgroup.append(col1)
    colgroup.append(col2)
    new_table.append(colgroup)

    # <tbody> 생성 및 데이터 행 추가
    tbody = soup.new_tag("tbody")
    for key, value in cs_info_dict.items():
        tr = soup.new_tag("tr")
        
        th = soup.new_tag("th")
        th.string = key
        tr.append(th)
        
        td = soup.new_tag("td")
        td.string = value
        tr.append(td)
        
        tbody.append(tr)
    
    new_table.append(tbody)
    break_agree_div.append(new_table)

    # .breakAgree_contents 아래에 새로운 .breakAgree03 추가
    break_agree_contents = soup.find("div", class_="breakAgree_contents")
    if break_agree_contents:
        break_agree_contents.append(break_agree_div)

# btnWrap 요소를 가장 하단으로 이동
btn_wrap = soup.find("div", class_="btnWrap")
if btn_wrap:
    btn_wrap.extract()  # btnWrap 요소를 제거하고
    break_agree_contents.append(btn_wrap)  # breakAgree_contents의 맨 마지막에 추가

# 변경된 HTML을 새로운 파일에 저장합니다.
with open('modify_text.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))