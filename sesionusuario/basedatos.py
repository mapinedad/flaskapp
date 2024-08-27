import pymysql
import hashlib


# Use this function for connect to the DB
def dame_conexion():
    return pymysql.connect(
        host='localhost',
        user='marcos',
        password='marcos123',
        db='basedatosflask'
    )

# Use this function to encrypt using SHA-256 the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Hash usando SHA-256

# Use this function for register a new user in the table usuarios
def alta_usuario(email, clave):
    conexion = dame_conexion()
    
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios(email, clave) VALUES (%s, %s)", (email, hash_password(clave))
            )
            conexion.commit()
    except pymysql.IntegrityError:
        print("Error: El email ya está registrado.")
        raise ValueError("El email ya está registrado.")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        raise
    finally:
        conexion.close()

def obtener_usuario(email):
    conexion = dame_conexion()
    usuarios = None

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT email, clave FROM usuarios WHERE email=%s", (email,)
            )
            usuario = cursor.fetchone()
    finally:
        conexion.close()
        return usuario

def obtener_registros():
    conexion = dame_conexion()
    usuarios = []

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT email FROM usuarios")
            usuarios = cursor.fetchall()
    finally:
        conexion.close()
        return usuarios

if __name__ == '__main__':
	alta_usuario('mapin232edad@gmail.com', '1234')
	print(obtener_usuario('mapin232edad@gmail.com'))
	usuarios = obtener_registros()
	print(usuarios)