#!/bin/bash
file_dir=/Users/koni114/gitRepo/TIL/Shell
if [ -d $file_dir ]; then
    echo "$file_dir 의 file 의 dir 이 존재합니다."
fi

file_dir=/Users/koni114/gitRepo/TIL/not_dir
if [ ! -d $file_dir ]; then
    echo "$file_dir 의 file 의 dir 이 존재하지 않습니다."
fi


