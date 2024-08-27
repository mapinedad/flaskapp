import pymysql

def connect():
	return pymysql.connect(
		host = 'localhost',
		user = 'marcos',
		password = 'marcos123',
		db = 'basedatosflask'
	)

def insertar_articulo(nombre, precio):
	conexion = connect()

	with conexion.cursor() as cursor:
		cursor.execute("INSERT INTO articulos(nombre,precio) VALUES (%s, %s)", (nombre, precio))
		conexion.commit()
		conexion.close()

def listar_articulos():
	conexion = connect()
	articulos = []

	with conexion.cursor() as cursor:
		cursor.execute("SELECT id, nombre, precio FROM articulos")
		articulos = cursor.fetchall()
		conexion.close()
		return articulos

def eliminar_articulo(id):
	conexion = connect()

	with conexion.cursor() as cursor:
		cursor.execute("DELETE FROM articulos WHERE id = %s", (id))
		conexion.commit()
		conexion.close()

def obtener_articulo(id):
	conexion = connect()
	articulo = None

	with conexion.cursor() as cursor:
		cursor.execute("SELECT id, nombre, precio FROM articulos WHERE id = %s", (id))
		articulo = cursor.fetchone()
		conexion.close()
		return articulo

def actualizar_articulo(id, nombre, precio):
	conexion = connect()

	with conexion.cursor() as cursor:
		cursor.execute("UPDATE articulos SET nombre = %s, precio = %s WHERE id = %s", (nombre, precio, id))
		conexion.commit()
		conexion.close()

if __name__ == '__main__':
	connect()
	print(listar_articulos())