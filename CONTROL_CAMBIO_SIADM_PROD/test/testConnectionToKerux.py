import cx_Oracle
import os

# Configuración de conexión a la base de datos
dsn = cx_Oracle.makedsn("172.17.32.109", 1521, service_name="KERUX")
user = "MAPINEDAD"
password = "S3n1a7mmiv"

# Ruta al directorio base en ADMIN
admin_path = r"C:\Users\MAPINEDAD\Documents\KENTRON\ADMIN"

def executeSQL(cursor, sql):
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Error ejecutando {sql}: {error.message}")

def connectToDB():
    # Buscar la carpeta en el directorio de administración
    folders = [f for f in os.listdir(admin_path) if os.path.isdir(os.path.join(admin_path, f)) and f.startswith("$ACT")]
    
    if not folders:
        print("No se encontró ninguna carpeta que comience con '$ACT' en el directorio de administración.")
        return
    
    # Supongamos que solo hay una carpeta que cumple con el criterio
    folder_name = folders[0]
    sql_file_path = os.path.join(admin_path, folder_name, "INSTALA_CAMBIOS.sql")
    
    if not os.path.exists(sql_file_path):
        print(f"No se encontró el archivo {sql_file_path}")
        return

    # Conexión a la base de datos
    connection = cx_Oracle.connect(user, password, dsn)
    cursor = connection.cursor()
    
    # Ejecutar el comando SQL para verificar el estado de la instancia
    executeSQL(cursor, "SELECT STATUS FROM V$INSTANCE")
    
    # Cerrar la conexión
    cursor.close()
    connection.close()
    print("Conexión cerrada.")

if __name__ == "__main__":
    connectToDB()
