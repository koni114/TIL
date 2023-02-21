num1=10
num2=30

if [ ${num1} -lt ${num2} ]; then
    echo "num1 이 num2 보다 작음"
fi

if (( $num1 < $num2 )); then
    echo "num1 이 num2 보다 작음"
fi  




