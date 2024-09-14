### Paso 1: Configurar Gunicorn para escuchar en la IP y puerto deseados
# Ejecuta Gunicorn con la opción `--bind` para especificar la IP y el puerto:

gunicorn --workers 3 --bind 10.156.80.115:6500 app:app

### Paso 2: Configurar `systemd` para Gunicorn
# Para asegurarte de que Gunicorn se ejecute siempre, incluso después de reiniciar el servidor, configura un archivo de servicio `systemd`.
#### Crear el archivo de servicio `systemd`

# Crea un archivo de servicio para Gunicorn en `/etc/systemd/system/pgbackrest_api.service`:
vi /etc/systemd/system/pgbackrest_api.service

# Añade lo siguiente al archivo (ajusta las rutas y nombres según tu configuración):
[Unit]
Description=Gunicorn instance to serve pgbackrest_api
After=network.target

[Service]
User=mapinedad
Group=mapinedad
WorkingDirectory=/home/mapinedad/pgbackrest_api
Environment="PATH=/home/mapinedad/pgbackrest_api/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/mapinedad/pgbackrest_api/venv/bin/gunicorn --workers 3 --bind 10.156.80.115:6500 app:app

[Install]
WantedBy=multi-user.target

#### Iniciar y habilitar el servicio de Gunicorn
# Inicia el servicio de Gunicorn y habilítalo para que se inicie al arrancar el sistema:
systemctl start pgbackrest_api
systemctl status pgbackrest_api
systemctl enable pgbackrest_api

### Paso 3: Verificar y probar
# Verifica que tu aplicación esté funcionando correctamente accediendo a la dirección `http://10.156.80.115:6500`. Puedes verificar el estado del servicio Gunicorn con:
systemctl status pgbackrest_api

### Paso4: Verificar funcionalidad de la api tanto para la stanza "seniat" como para la stanza "psuv"
# Las rutas (url) de la api son:

# SENIAT
http://10.156.80.115:6500/api/seniat/backups			# Muestra un json con la información de los backups realizados.
http://10.156.80.115:6500/api/seniat/backups/last		# Información sobre el útltimo backup realizado en el día.
http://10.156.80.115:6500/api/seniat/status				# Información sobre la salud de la Stanza y conectividad con los nodos de BD.
http://10.156.80.115:6500/api/seniat/check_archives 	# Verificación de los archives de los backups que se han hecho.
http://10.156.80.115:6500/api/seniat/check_retention	# Verificación de las políticas de retención.

# PSUV
http://10.156.80.115:6500/api/psuv/backups			# Muestra un json con la información de los backups realizados.
http://10.156.80.115:6500/api/psuv/backups/last		# Información sobre el útltimo backup realizado en el día.
http://10.156.80.115:6500/api/psuv/status			# Información sobre la salud de la Stanza y conectividad con los nodos de BD.
http://10.156.80.115:6500/api/psuv/check_archives 	# Verificación de los archives de los backups que se han hecho.
http://10.156.80.115:6500/api/psuv/check_retention	# Verificación de las políticas de retención.