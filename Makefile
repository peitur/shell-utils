

venv:
	virtualenv --no-wheel --no-setuptool .

clean:
	rm -fR lib \
	pyvenv.cfg \
	bin/activate* \
	bin/easy_install* \
	bin/pip* \
	bin/python* \
	bin/wheel* 
