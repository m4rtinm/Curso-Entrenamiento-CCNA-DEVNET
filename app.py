from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__)

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (nombre TEXT, apellido TEXT, correo TEXT, password_hash TEXT)''')
    conn.commit()
    conn.close()

# Función para hashear la contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo'] 
        password = request.form['password']
        password_hash = hash_password(password)

        conn = sqlite3.connect('usuarios.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (nombre, apellido, correo, password_hash) VALUES (?, ?, ?, ?)", 
                  (nombre, apellido, correo, password_hash))
        conn.commit()
        conn.close()

        return 'Usuario registrado correctamente'
    else:
        return '''
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f2f2f2;
                    }
                    .form-container {
                        width: 300px;
                        padding: 20px;
                        background-color: white;
                        margin: 100px auto;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    h2 {
                        text-align: center;
                    }
                    input[type="text"], input[type="password"], input[type="email"] {
                        width: 100%;
                        padding: 10px;
                        margin: 8px 0;
                        box-sizing: border-box;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                    input[type="submit"] {
                        width: 100%;
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px;
                        margin: 8px 0;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <div class="form-container">
                    <h2>Registro de Usuario</h2>
                    <form method="post">
                        Nombre: <input type="text" name="nombre" required><br>
                        Apellido: <input type="text" name="apellido" required><br>
                        Correo electrónico: <input type="email" name="correo" required><br>
                        Contraseña: <input type="password" name="password" required><br>
                        <input type="submit" value="Registrar">
                    </form>
                </div>
            </body>
            </html>
        '''

@app.route('/usuarios')
def listar_usuarios():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute("SELECT nombre, apellido, correo, password_hash FROM users")
    rows = c.fetchall()
    conn.close()
    return str(rows)

if __name__ == '__main__':
    init_db()
    app.run(port=7890)
