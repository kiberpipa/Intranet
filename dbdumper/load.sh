#!/bin/bash

APPS="contenttypes auth www org tags wiki sites flatpages admin markup"

PYTHONPATH=`pwd`/../libs:`pwd`/.. ./db_dump.py -v --settings=intranet.settings -d dbdump load $APPS
