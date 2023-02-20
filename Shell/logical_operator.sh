file1=test.sh 
file2=var_type.sh

if [ -f ${file1} -a -f ${file2} ]; then
    echo "File1 과 File2 는 모두 파일입니다."
else
    echo "file1 과 file2 가 모두 파일인 것은 아닙니다."
fi
