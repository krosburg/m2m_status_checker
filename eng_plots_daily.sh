#!/bin/bash

# VARIABLES
LOGFILE=$HOME/logs/engm2m_data_daily.log

# Run Engineering Plotter
date > $LOGFILE
cd $HOME/m2m_status_checker
$HOME/miniconda3/bin/python plotEngineeringM2M.py day >> $LOGFILE

# Check for Errors
MSG="Success"
STATUS=0
if [ -f ./eng_fail.flag ]; then
    /usr/bin/mail -s "[M2M Status]: Engineering Plot Failure" krosburg@uw.edu < eng_fail.flag
    STATUS=2
    MSG=$(cat eng_fail.flag | tr '\n' ' ')
fi

# Update SysDash Database
mysql dash -e "UPDATE script_status SET status=${STATUS}, ts=NULL, note='${MSG}' WHERE name = 'M2M Eng Plotter'"
echo "Completed." >> $LOGFILE



