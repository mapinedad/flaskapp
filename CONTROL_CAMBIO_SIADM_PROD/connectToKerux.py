import cx_Oracle
import os
from loadCredentialsPaths import load_paths


# Ruta al archivo de rutas
paths_path = 'C:\\Users\\mapinedad\\Documents\\work_scripts\\PYTHON\\CONTROL_CAMBIO_SIADM_PROD\\paths\\paths.json'

# Cargar rutas
paths = load_paths(paths_path)

# Configuración de conexión a la base de datos
# dsn = cx_Oracle.makedsn("172.17.32.109", 1521, service_name="KERUX")
# admin_user = "MAPINEDAD"
# admin_password = "S3n1a7mmiv"
# gob_user = "gob"
# gob_password = "gob"

# Acceder a las credenciales de la base de datos
dsn = credentials['database']['dsn']
admin_user = credentials['database']['admin_user']
admin_password = credentials['database']['admin_password']
gob_user = credentials['database']['gob_user']
gob_password = credentials['database']['gob_password']

# Ruta al directorio base en ADMIN
# admin_path = r"C:\Users\MAPINEDAD\Documents\KENTRON\ADMIN"
admin_path = paths['admin_directory']


def executeSQL(cursor, sql):
    try:
        cursor.execute(sql)
        print(f"Ejecutado: {sql}")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Error ejecutando {sql}: {error.message}")

def executeSQLFile(cursor, file_path):
    if not os.path.exists(file_path):
        print(f"No se encontró el archivo {file_path}")
        return

    with open(file_path, 'r') as sql_file:
        sql_commands = sql_file.read().split(';')
        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command.strip())
                    print(f"Ejecutado: {command.strip()}")
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    print(f"Error ejecutando {command.strip()}: {error.message}")

def connectToDB():
    # Buscar la carpeta en el directorio de administración
    folders = [f for f in os.listdir(admin_path) if os.path.isdir(os.path.join(admin_path, f)) and f.startswith("$ACT")]
    
    if not folders:
        print("No se encontró ninguna carpeta que comience con '$ACT' en el directorio de administración.")
        return
    
    # Supongamos que solo hay una carpeta que cumple con el criterio
    folder_name = folders[0]
    instala_cambios_path = os.path.join(admin_path, folder_name, "INSTALA_CAMBIOS.sql")
    grant_syns_path = os.path.join(admin_path, "GRANTSYNS.sql")
    recomp_path = os.path.join(admin_path, "RECOMP.sql")

    # Conexión a la base de datos con el usuario admin
    connection = cx_Oracle.connect(admin_user, admin_password, dsn)
    cursor = connection.cursor()
    
    # Ejecutar 'ALTER USER' para cambiar la contraseña del usuario gob
    executeSQL(cursor, "ALTER USER gob IDENTIFIED BY gob")
    
    # Cerrar la conexión admin
    cursor.close()
    connection.close()

    # Conexión a la base de datos con el usuario gob
    connection = cx_Oracle.connect(gob_user, gob_password, dsn)
    cursor = connection.cursor()

    # Leer y ejecutar el contenido del archivo INSTALA_CAMBIOS.sql
    executeSQLFile(cursor, instala_cambios_path)

    # Leer y ejecutar el contenido de los archivos GRANTSYNS.sql y RECOMP.sql
    executeSQLFile(cursor, grant_syns_path)
    executeSQLFile(cursor, recomp_path)
    
    # Confirmar los cambios
    connection.commit()
    
    # Cerrar la conexión gob
    cursor.close()
    connection.close()
    print("Conexión cerrada y cambios confirmados.")

    # Conexión a la base de datos con el usuario admin para colocar la contraseña original al user GOB
    connection = cx_Oracle.connect(admin_user, admin_password, dsn)
    cursor = connection.cursor()

    # Ejecutar 'ALTER USER' para cambiar la contraseña del usuario gob
    executeSQL(cursor, "ALTER USER gob IDENTIFIED BY asturias")
    
    # Cerrar la conexión admin
    cursor.close()
    connection.close()
    

if __name__ == "__main__":
    connectToDB()