#!/bin/bash

# The actual path to the Python script.
APP_PATH="/home/wikivisor/WebstormProjects/pdf-citation-highlighter/server.py"
PID_FILE="/var/run/pdf-citation-highlighter.pid"

start() {
    if [ -f $PID_FILE ]; then
        echo "The service is already running."
    else
        nohup python $APP_PATH &> /dev/null &
        echo $! > $PID_FILE
        echo "Service started."
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        kill $(cat $PID_FILE)
        rm $PID_FILE
        echo "Service stopped."
    else
        echo "The service is not running."
    fi
}

restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
esac
