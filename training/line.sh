for J in `ls $1`;
do
	for D in `ls systems`;
	do 
		wc -l $1/$J/result_$D ;
	done ;
done

