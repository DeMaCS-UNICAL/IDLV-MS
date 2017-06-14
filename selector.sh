#!/bin/bash

FILTER=$1

DIR=`dirname $0`;
FILE=$DIR/enigma.$$;
touch $FILE;
INST="";

IDLV="$DIR/idlv-lpopt-portable/idlv --stdin --enable-lpopt --filter=$FILTER"
if [[ $FILTER = "show_all" ]];then
    IDLV="$DIR/idlv-lpopt-portable/idlv --stdin --enable-lpopt"
fi


DATA=$(cat $INST | $IDLV 2> /dev/null | $DIR/freader/NumericOut $FILE )

CLASP="$DIR/clingo-5.1 --mode=clasp --configuration=trendy --outf=1"
WASP="$DIR/wasp-05-04-2017 --competition-output --trim-core --enable-disjcores --shrinking-strategy=progression --shrinking-budget=10"
EXITCODE=1
trap ":" 24 15

SOLVER=$(echo $DATA | $DIR/dist/selector/selector)
if [[ $SOLVER == *"wasp"* ]]; then
    echo $IDLV $WASP >> $DIR/log
    cat $FILE | $WASP
    EXITCODE=$?
else
    echo $IDLV $CLASP >> $DIR/log
    cat $FILE | $CLASP
    EXITCODE=$?
fi

rm $FILE
exit $EXITCODE
