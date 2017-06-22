#!/bin/bash
MOD=$(echo $1 | cut -d_ -f2)
 M1=$(echo $1 | cut -d_ -f3)
 M2=$(echo $1 | cut -d_ -f4)
( cd $1 && \
combineCards.py $(for f in 2los_*txt; do echo $(echo $f | sed -e 's/2los_\|_unblind.card.txt//g')=$f; done ) > comb.txt && \
text2workspace.py comb.txt && \
combine -M Asymptotic comb.root -n ${MOD} -m ${M1} -s ${M2} )
