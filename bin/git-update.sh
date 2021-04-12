#!/bin/bash

CPWD=${PWD}
for X in $( ls -1 ${CPWD} ); do
	if [[ -d ${CPWD}/${X} ]]; then
		echo "INFO: Checking ${X}"
		if [[ -d ${CPWD}/${X}/.git ]]; then
			cd ${CPWD}/$X
			git pull
			cd -
		fi
	fi
done
