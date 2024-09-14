import json


def load_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials

"""# Ruta al archivo de credenciales
credentials_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\credentials.json'

# Cargar credenciales
credentials = load_credentials(credentials_path)

# Acceder a las credenciales de la base de datos
dsn = credentials['database']['dsn']
admin_user = credentials['database']['admin_user']
admin_password = credentials['database']['admin_password']
gob_user = credentials['database']['gob_user']
gob_password = credentials['database']['gob_password']

# Acceder a las credenciales del servidor
server_host = credentials['server']['host']
server_user = credentials['server']['user']
server_password = credentials['server']['password']"""

def load_paths(file_path):
    with open(file_path, 'r') as file:
        paths = json.load(file)
    return paths

"""# Ruta al archivo de rutas
paths_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\paths.json'

# Cargar rutas
paths = load_paths(paths_path)

# Acceder a las rutas
extracted_directory = paths['extracted_directory']
admin_path = paths['admin_path']"""