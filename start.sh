#!/bin/bash

# Actualizar e instalar dependencias necesarias
apt-get update && apt-get install -y gnupg2 curl software-properties-common build-essential

# Agregar claves e instalar repositorio de Microsoft para los drivers
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update

# Aceptar el EULA e instalar el driver ODBC para SQL Server
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Verificar instalación del driver y registrar en logs
odbcinst -j
ls /opt/microsoft/msodbcsql17

# Limpiar cache para reducir el tamaño del contenedor
apt-get clean

# Iniciar la aplicación con Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
