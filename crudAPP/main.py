from flask import Flask, redirect, render_template, request, url_for
import basedatos as bd

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/agregar_articulo')
def agregar_articulo():
	return render_template("agregar_articulo.html")

@app.route('/guardar_articulo', methods=['POST'])
def guardar_articulo():
	nombre = request.form['nombre']
	precio = request.form['precio']

	bd.insertar_articulo(nombre, precio)

	return redirect('/articulos')

@app.route('/')
@app.route('/articulos')
def articulos():
	articulos = bd.listar_articulos()
	return render_template('articulos.html', articulos=articulos)

@app.route('/eliminar_articulo', methods=['POST'])
def eliminar_articulo():
	bd.eliminar_articulo(request.form['id'])
	return redirect("/articulos")

@app.route("/editar_articulo/<int:id>")
def editar_articulo(id):
	articulo = bd.obtener_articulo(id)
	return render_template("editar_articulo.html", articulo=articulo)

@app.route("/actualizar_articulo", methods=['POST'])
def actualizar_articulo(id):
	id = request.form["id"]
	nombre = request.form["nombre"]
	precio = request.precio["precio"]

	bd.actualizar_articulo(id, nombre, precio)
	return redirect("/articulos")

if __name__ == '__main__':
    app.run(debug=True)