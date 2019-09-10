for u in spez BennyFeldman whiskeysquid
do
	python data_reddit.py -user $u &
done
wait