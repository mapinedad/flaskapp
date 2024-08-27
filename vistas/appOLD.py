from flask import Flask, render_template

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/saludo/<string:nombre>')
def saludo(nombre: str):
	return f"""
		<h1>Hola, {nombre}, un gusto saludarte!</h1>
		<h3>Estamos en el tutorial de Flask de Python</h3>
	"""

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


if __name__ == '__main__':
	app.run(debug=True)