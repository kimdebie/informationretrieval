#!/bin/sh

h=$1
h=${h: -1}
puzzle=$2

if [ "$h" = "2" ]; then
    heuristic="MOMS"
elif [ "$h" = "3" ]
then
    heuristic="JW"
elif [ "$h" = "4" ]
then
    heuristic="JWTS"
elif [ "$h" = "5" ]
then
    heuristic="nishio"
else
    heuristic="random"
fi

echo "$puzzle"
echo "$heuristic"

python SAT.py "$heuristic" "$puzzle"
