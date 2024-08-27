from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__, template_folder='template')

@app.before_request
def before_request():
	print("Antes del request")

@app.after_request
def after_request(response):
	print("Despues del request")
	return response

@app.route('/')
def index():
	flash('ESTAS EN EL INDEX DEL PROYECTO FLASK')
	print("Accediendo al index o ppal page")
	diccionario = {'title':'Página de Inicio - Empresa XYZ', 'encabezado':'Bienvenido a Empresa XYZ'}
	return render_template('index.html', datos=diccionario)

@app.route('/redirecciona')
@app.route('/redirecciona/<string:sitio>')
def redirecciona(sitio=None):
	if sitio is not None:
		return redirect(url_for('index'))
	else:
		return redirect(url_for('about'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contacto')
def contacto():
	return render_template('contacto.html')

@app.route('/productos')
def productos():
	return render_template('productos.html')

@app.route('/servicios')
def servicios():
	return render_template('servicios.html')

@app.route('/condicionybucle/<int:age>')
def condicionybucle(age=50):
	edad = age
	return render_template('condicionybucle.html', dato = edad)

def pagina_no_encontrada(error):
	return render_template('errores/404.html'), 404


if __name__ == '__main__':
	app.register_error_handler(404, pagina_no_encontrada)
	app.secret_key = 'clave-flask'
	app.run(debug=True)