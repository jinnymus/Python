#!/usr/bin/env bash
for a in {1..10000}
do
#echo "a: "$a
cat bigfile >> bigfile_2
done