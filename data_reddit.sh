for u in spez BennyFeldman whiskeysquid
do
	python data_reddit.py -user $u -num-comments 1000 &
done
wait