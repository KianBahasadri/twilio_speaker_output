#!/bin/bash

source venv/bin/activate

while true
do
	fastapi run server.py --port 5000 2>&1 >> /var/log/fastapi.log
done
