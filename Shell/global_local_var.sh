# 기본적으로 전역 변수로 지정됨
string="hello world"

function string_test(){
    # local 을 붙여야 지역변수로 인식. 만일 local 을 빼면 전역변수 덮어쓰기가 되버림
    local string="hello local ! "
    echo ${string}
}

string_test
echo ${string}

# 변수 초기화
unset string