#!/bin/bash

# 단순 문자열 출력
echo date

# 백틱으로 감싸주면 date 명령어가 실행되게 됨
echo `date`

# $() 도 마찬가지임
echo $(date)

# shell execution
echo "I'm in `pwd`"
echo "I'm in $(pwd)"


