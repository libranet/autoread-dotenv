# See ../makefile


.PHONY: python-which  ## show which python is used
python-which:
	@ which python


.PHONY: pip-which  ## show which pip is used
pip-which:
	@ which pip


.PHONY: pip-upgrade ## upgrade pip itself
pip-upgrade: python-which
	 python -m pip install --upgrade pip