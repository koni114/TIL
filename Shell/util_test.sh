#!/bin/bash
count2=10
until (( ${count2} <= 5 ));
do
    echo ${count2}
    count2=$(( ${count2} - 1 ))
done
