#!/bin/bash
result=`echo $PWD | grep -o -e ^.*\/Expona`
cd $result
echo "Starting Expona."
python -m webrest.api
