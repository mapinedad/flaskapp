from flask import Flask

app = Flask(__name__)

@app.route("/")
def hola():
	return "<h1>Hola Mundo! <br>con FLask</h1><br><h2>WHAT?</h2>"