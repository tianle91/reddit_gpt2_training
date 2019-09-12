for u in spez BennyFeldman whiskeysquid
do
	python -u get_training.py -user $u -num-comments 1000 >"log/$u.log"
	python pack_training.py -user $u
done
