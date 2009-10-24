#!/bin/bash

PYTHONPATH=`pwd`/..:`pwd`/../libs:`pwd`/../intranet ./db_dump.py -v --settings=intranet.settings -d dbdump/ dump

tar jcvf ~/dbdump.tar.bz2 dbdump

rm -rf dbdump
