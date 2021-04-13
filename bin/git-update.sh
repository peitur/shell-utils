#!/bin/bash

XPWD=${PWD}
ARGS="$@"

if [[ $# == 0 ]]; then
	ARGS="."
fi

for V in ${ARGS[@]}; do

	CPWD="${XPWD}/$V"
	echo "[ ] INFO: Checking everything in ${CPWD}"

	for X in $( ls -1 ${CPWD} ); do
		if [[ -d ${CPWD}/${X} ]]; then
			echo "[+] INFO: Checking ${CPWD}/${X}"
			if [[ -d ${CPWD}/${X}/.git ]]; then
				cd ${CPWD}/$X
				git pull
				cd ${CPWD}
			fi
		fi
	done

done
