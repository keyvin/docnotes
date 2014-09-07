#!/bin/bash

if [ $1 == '' ]; then  
    echo 'Please supply a file name';
fi

#echo 'Totalling the file'

list=$(cat $1 | cut -f2)

total=0

for i in $list; do total=$(( $total + $i )); done

echo $total



