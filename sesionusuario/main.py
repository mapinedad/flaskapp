from flask import Flask, redirect, request, url_for, render_template, flash, session
import basedatos
import hashlib

app = Flask(__name__)
app.secret_key = 'miclavesecreta'

@app.before_request
def antes_de_todo():
    ruta = request.path
    if not 'usuario' in session and ruta not in ["/entrar", "/login", "/salir", "/registro", "/usuarios"]:
        flash("Inicia sesión para continuar")
        return redirect("/entrar")

@app.route("/dentro")
def dentro():
    return render_template("index.html")

@app.route("/")
@app.route("/entrar")
def entrar():
    return render_template("entrar.html")

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    contrasena = request.form['contrasena']

    try:
        usuario = basedatos.obtener_usuario(email)
    except Exception as e:
        flash("Error al obtener usuario: " + str(e))
        return redirect("/entrar")

    if usuario:
        # Verificar la contraseña
        if usuario[1] == basedatos.hash_password(contrasena):
            session['usuario'] = email
            return redirect("/dentro")
        else:
            flash("Acceso denegado: contraseña incorrecta")
            return redirect("/entrar")
    else:
        flash("Acceso denegado: usuario no encontrado")
        return redirect("/entrar")

@app.route("/salir")
def salir():
    session.pop("usuario", None)
    flash("Sesión cerrada")
    return redirect("/entrar")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/registrar", methods=['POST'])
def registrar():
    email = request.form['email']
    contrasena = request.form['contrasena']

    # Verificar si el usuario ya existe
    if basedatos.obtener_usuario(email):
        flash("El usuario ya está registrado.")
        return redirect("/registro")

    try:
        basedatos.alta_usuario(email, contrasena)
        flash("Usuario registrado exitosamente")
    except ValueError as ve:
        flash(str(ve))  # Mensaje de error específico
    except Exception as e:
        flash("Error al registrar usuario: " + str(e))
        print("Error al registrar usuario:", e)  # Imprimir el error en la consola para depuración
    finally:
        return redirect("/entrar")

@app.route("/usuarios")
def mostrar_usuarios():
    try:
        usuarios = basedatos.obtener_registros()
        return render_template("usuarios.html", usuarios=usuarios)
    except Exception as e:
        flash("Error al obtener usuarios: " + str(e))
        return redirect("/entrar")

if __name__ == '__main__':
    app.run(debug=True)