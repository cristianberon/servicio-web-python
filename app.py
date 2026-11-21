
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Almacena los usuarios mientras el servicio está activo.
usuarios = {}


# Endpoint para registrar un usuario.
@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True)

    # Verifica que los datos tengan formato JSON de objeto.
    if not isinstance(datos, dict):
        return jsonify({"mensaje": "Los datos deben enviarse en formato JSON"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    # Verifica que los campos sean cadenas de texto válidas.
    if (
        not isinstance(usuario, str)
        or not usuario.strip()
        or not isinstance(contraseña, str)
        or not contraseña
    ):
        return jsonify({"mensaje": "Faltan datos o son inválidos"}), 400

    usuario = usuario.strip()

    if usuario in usuarios:
        return jsonify({"mensaje": "El usuario ya existe"}), 400

    # Protege la contraseña antes de almacenarla.
    usuarios[usuario] = generate_password_hash(contraseña)

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


# Endpoint para iniciar sesión.
@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True)

    # Verifica que los datos tengan formato JSON de objeto.
    if not isinstance(datos, dict):
        return jsonify({"mensaje": "Los datos deben enviarse en formato JSON"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if (
        not isinstance(usuario, str)
        or not usuario.strip()
        or not isinstance(contraseña, str)
        or not contraseña
    ):
        return jsonify({"mensaje": "Faltan datos o son inválidos"}), 400

    usuario = usuario.strip()

    # Comprueba que el usuario y la contraseña sean correctos.
    if (
        usuario in usuarios
        and check_password_hash(usuarios[usuario], contraseña)
    ):
        return jsonify({"mensaje": "Autenticación satisfactoria"}), 200

    return jsonify({"mensaje": "Autenticación fallida"}), 401


# Inicia el servicio web local.
if __name__ == "__main__":
    app.run(debug=False)

