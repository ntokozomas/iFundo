#!/bin/bash

# --------------------------------------------------
# iFundo Startup Script
# --------------------------------------------------

LOGFILE="startup.log"
VENV_PATH="/home/pi/ifundo/venv"      
APP_PATH="/home/pi/ifundo/start_ifundo.py"  

echo "[$(date)] Starting iFundo initialization..." >> $LOGFILE

echo "[$(date)] Checking virtual environment..." >> $LOGFILE
sleep 2

echo "[$(date)] Activating virtual environment..." >> $LOGFILE
source "$VENV_PATH/bin/activate"
sleep 2

echo "[$(date)] Verifying dependencies..." >> $LOGFILE
pip list >> $LOGFILE
sleep 2

echo "[$(date)] Launching iFundo application..." >> $LOGFILE
python3 "$APP_PATH" >> $LOGFILE 2>&1 &
sleep 2

echo "[$(date)] iFundo startup sequence complete." >> $LOGFILE
exit 0
