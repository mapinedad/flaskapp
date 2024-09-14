import paramiko
import os
import time
import shutil
import subprocess
from loadCredentialsPaths import *
# from loadCredentialsPaths import load_credentials, load_paths


# Ruta al archivo de credenciales y paths
credentials_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\credentials\\credentials.json'
paths_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\paths\\paths.json'

# Cargar credenciales y paths
credentials = load_credentials(credentials_path)
paths = load_paths(paths_path)

# Configuración de conexión SSH
# ssh_host = "172.16.16.126"
# ssh_user = "oas"
# ssh_password = "126n01_oas"
server_host = credentials['server']['host']
server_user = credentials['server']['user']
server_password = credentials['server']['password']

down_script = "/home/oas/scripts/down.sh"
start_script = "/home/oas/scripts/start.sh"


# Ruta al script de base de datos
# db_script_path = r"C:\Users\mapinedad\Documents\work_scripts\PYTHON\CONTROL_CAMBIO_SIADM_PROD\connectToKerux.py"
db_script_path = paths['db_script_dir']

# Rutas locales
admin_path = paths['admin_path']
realizado_path = paths['done_dir']


def run_ssh_command(ssh_client, command):
	stdin, stdout, stderr = ssh_client.exec_command(command)
	stdout.channel.recv_exit_status()  # Esperar a que el comando termine
	return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

def run_db_script():
	# Ejecutar el script de base de datos
	result = subprocess.run(["python", db_script_path], capture_output=True, text=True)
	print("Salida del script de base de datos:")
	print(result.stdout)
	if result.stderr:
		print("Errores del script de base de datos:")
		print(result.stderr)

def move_act_folder():
	# Buscar la carpeta en el directorio de administración
	folders = [f for f in os.listdir(admin_path) if os.path.isdir(os.path.join(admin_path, f)) and f.startswith("$ACT")]
	
	if not folders:
		print("No se encontró ninguna carpeta que comience con '$ACT' en el directorio de administración.")
		return

	# Supongamos que solo hay una carpeta que cumple con el criterio
	folder_name = folders[0]
	source_folder = os.path.join(admin_path, folder_name)
	destination_folder = os.path.join(realizado_path, folder_name)

	# Copiar la carpeta al directorio 'realizado'
	shutil.copytree(source_folder, destination_folder)
	print(f"Carpeta {folder_name} copiada a {realizado_path}.")
			
	# Eliminar la carpeta del directorio de ADMIN
	shutil.rmtree(source_folder)
	print(f"Eliminada la carpeta {folder_name} del directorio de extracción.")

def connectToSIADM():
	# Conexión SSH al servidor remoto
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(server_host, username=server_user, password=server_password)

	print("Ejecutando down.sh en el servidor remoto...")
	stdout, stderr = run_ssh_command(ssh_client, f"/bin/bash {down_script}")
	print(stdout)
	if stderr:
		print(f"Errores ejecutando down.sh: {stderr}")
	
	# Esperar unos segundos para asegurar que el down.sh ha terminado completamente
	time.sleep(15)

	# Ejecutar el script de base de datos
	run_db_script()

	print("Ejecutando start.sh en el servidor remoto...")
	stdout, stderr = run_ssh_command(ssh_client, f"/bin/bash {start_script}")
	print(stdout)
	if stderr:
		print(f"Errores ejecutando start.sh: {stderr}")

	ssh_client.close()
	
	# Mover la carpeta cuyo nombre comienza con $ACT a 'realizado'
	move_act_folder()


if __name__ == "__main__":
	connectToSIADM()