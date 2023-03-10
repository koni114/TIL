#!/bin/bash

# expr 는 역따옴표를 반드시 감싸준다. 역따옴표 대신 $(()) 해줘도 동작은 함
# expr 을 사용할 때 피연산자와 연산자 사이에 공백이 필요
# 산술 연산할 때 우선순위를 지정하기 위해 괄호를 사용하려면 \처리를 해줘야 함
# 곱셈 문자 *는 \처리를 해주어야 함

number1=10
number2=20

plus=`expr $number1 + $number2`
minus=`expr $number1 - $number2`
mul=`expr $number1 \* $number2` # 곱셈에는 \* 를 이용
div=`expr $number1 / $number2`
rem=`expr $number1 % $number2`

echo "plus:      ${plus}"
echo "minus:     ${minus}"
echo "mul:       ${mul}"
echo "div:       ${div}"
echo "rem:       ${rem}"

