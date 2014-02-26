#!/bin/bash

RET=0

flake8 keyhub
RET=$(($RET+$?))

nosetests keyhub
RET=$(($RET+$?))

exit $RET
