for u in spez BennyFeldman whiskeysquid
do
	nohup python -u get_training.py -user $u -num-comments 1000 >"log/$u.log" &
done
