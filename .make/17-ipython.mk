# See ../makefile


.PHONY: ipython-symlink-to-ip  ## symlink bin/ipython to bin/ip
ipython-symlink-to-ip:
	- cd .venv/bin && ln -s ipython ip && cd -

