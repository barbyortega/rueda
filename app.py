from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import ConfiguracionBd
from RuedaSolidaria.controlador.usuario_controlador import usuarios_bp
import os  # Importa el módulo os

app = Flask(__name__)
app.config.from_object(ConfiguracionBd)

# Cargar la configuración de la base de datos desde 'ConfiguracionBd'
app.config.from_object(ConfiguracionBd)

# Registrar el blueprint de usuarios
app.register_blueprint(usuarios_bp)

# Definir la clave secreta para manejar sesiones
app.secret_key = 'clave_secreta_super_segura'

# Usuarios simulados (normalmente estos datos se manejarían en la base de datos)
usuarios = {
    "barby": "barby1006",
    "admin": "adminpass"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and usuarios[username] == password:
            session['usuario'] = username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('perfil'))  
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/perfil')  
def perfil():
    if 'usuario' in session:
        usuario = session['usuario']
        return render_template('perfil.html', usuario=usuario)  
    else:
        flash('Necesitas iniciar sesión primero', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('¡Sesión cerrada!', 'info')
    return redirect(url_for('index'))

# Imprime el directorio de trabajo actual
if __name__ == '__main__':
    print(os.getcwd())  # Imprime el directorio de trabajo actual
    app.run(debug=True)
