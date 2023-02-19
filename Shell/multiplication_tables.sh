#!/bin/bash

for (( i = 1; i < 10; i++ ))
do
    echo "Outer Loop -> $i"
    for (( j = 1; j < 10; j++ ))
    do
        (( result = $i \* $j ))
        echo "$i X $j = $result"
    done
done

