#!/bin/bash

# Instalar las dependencias necesarias
apt-get update && apt-get install -y gnupg2 curl software-properties-common

# Agregar las claves e instalar el repositorio de Microsoft para los drivers
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update

# Aceptar el EULA e instalar el driver ODBC para SQL Server
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Limpiar para reducir el tamaño del contenedor
apt-get clean

# Iniciar Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
