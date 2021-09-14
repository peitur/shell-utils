#!/bin/bash

TORSTRING="torservers.net"

if [[ ! $1 ]]; then
  echo "Missing IP"
  exit 0
fi

if dig +short -x $1|grep ${TORSTRING} >> /dev/null; then
  echo "True"
  exit 0
else
  echo "False"
  exit 1
fi
