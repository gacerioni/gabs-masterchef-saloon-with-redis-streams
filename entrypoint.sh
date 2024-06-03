#!/bin/sh

# Check the first argument and run the corresponding script
if [ "$1" = "producer" ]; then
    python /usr/src/app/producer/producer.py
elif [ "$1" = "consumer" ]; then
    if [ -z "$2" ]; then
        echo "Error: Consumer name not provided"
        exit 1
    fi
    python /usr/src/app/consumer/consumer.py "$2"
elif [ "$1" = "supervisor" ]; then
    python /usr/src/app/supervisor/supervisor.py
else
    echo "Error: Unknown command"
    echo "Usage: $0 {producer|consumer <name>|supervisor}"
    exit 1
fi