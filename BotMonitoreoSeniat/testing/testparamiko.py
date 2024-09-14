import paramiko

# Crear una instancia de SSHClient
ssh = paramiko.SSHClient()

# Cargar las claves del sistema (puedes personalizar esto según tus necesidades)
ssh.load_system_host_keys()

# Agregar la clave del servidor (puedes proporcionar la clave directamente o usar un archivo de clave)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Conectar al servidor SSH
ssh.connect('172.16.32.67', port=22252, username='oracle', password='Or49iCygP')

# Ejecutar un comando remoto
stdin, stdout, stderr = ssh.exec_command('ls')

# Imprimir la salida del comando
print(stdout.read().decode())

# Cerrar la conexión SSH
ssh.close()
