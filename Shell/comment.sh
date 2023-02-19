#!/bin/bash
echo "여기는 출력됩니다."
# 여기는 주석 처리 됩니다.

: << "END"  # 주석 시작
echo "여기서부터"
echo "계속 주석 처리됨"
END

echo "여기는 주석이 안되어 있어서 출력"

name="JaeHun"
pass=123123
let re=pass*10
echo $re