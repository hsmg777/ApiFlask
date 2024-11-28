#!/bin/bash
apt-get update && \
apt-get install -y gnupg2 curl && \
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
apt-get update && \
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev && \
apt-get clean

gunicorn app:app --bind 0.0.0.0:$PORT
