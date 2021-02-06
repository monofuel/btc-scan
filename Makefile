
.PHONY: check
check:
	python3 -m py_compile mount-drives.py
	python3 -m py_compile folder-scan.py
	python3 -m py_compile byte-scan.py
