#!/bin/bash
count=10
while (( ${count} >  5 ));
do
    echo $count
    count=$(( ${count} - 1 ))
done