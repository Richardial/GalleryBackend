from flask import Flask,jsonify, request
from flask_cors import CORS, cross_origin
import psycopg2

url = "postgresql://fotosdelmundo_user:S4dex9mXbosCUXY6ApTUifP75KwhwuYq@dpg-csvrl6i3esus73831na0-a.oregon-postgres.render.com/fotosdelmundo"
# url = "postgresql://postgres:1234@localhost:5432/fotosdelmundo"

app = Flask(__name__)
cors = CORS(app,supports_credentials=True)
CORS(app, resources={
    r"/login/*": {"origins": ["http://localhost:5173", "https://fotosdelmundo.netlify.app"]},
    r"/register/*": {"origins": ["http://localhost:5173", "https://fotosdelmundo.netlify.app"]},
    r"/credentials/*": {"origins": ["http://localhost:5173", "https://fotosdelmundo.netlify.app"]},
}, supports_credentials=True)

app.config['CORS_HEADERS'] = 'Content-Type'
connection = psycopg2.connect(url)

# INSERT_NEW_USER = ("INSERT INTO registros(nombre,apellido,contrasena,correo) values (%s,%s,%s,%s)")
INSERT_NEW_USER = ("INSERT INTO registros(nombre,apellido,contrasena,correo) values ('{0}','{1}','{2}','{3}')")
# GET_CREDENTIALS = ("SELECT correo, contrasena FROM registros WHERE correo = %s AND contrasena = %s")
GET_CREDENTIALS = ("SELECT correo, contrasena FROM registros WHERE correo = '{0}' AND contrasena = '{1}'")
GET_CREDENTIALS2 = ("SELECT nombre, apellido, correo, contrasena FROM registros WHERE correo = '{0}' AND contrasena = '{1}'")


@app.route("/")
def home():
    return "Todo piola"


@app.route("/register", methods=["POST"])
def create_user():
    data_json = request.get_json(force=True)
    nombre = data_json["nombre"]
    print(nombre)
    apellido = data_json["apellido"]
    contrasena = data_json["contrasena"]
    correo = data_json["correo"]
    with connection:
        with connection.cursor() as cursor:
            # cursor.execute(INSERT_NEW_USER, (nombre,apellido,contrasena,correo))
            cursor.execute(INSERT_NEW_USER.format(nombre,apellido,contrasena,correo))
    return jsonify(["Working"])


@app.route("/login", methods=["POST"])
def login():
    data_json = request.get_json(force=True)
    correo = data_json["correo"]
    contrasena = data_json["contrasena"]
    with connection:
        with connection.cursor() as cursor:
            print("Ejecutando consulta:", cursor.mogrify(GET_CREDENTIALS.format(correo,contrasena)))
            cursor.execute(GET_CREDENTIALS.format(correo,contrasena))
            credentials = cursor.fetchone()
    if credentials is not None:
        return jsonify(credentials)
    else:
        
        return "Usuario o contraseña erroneos",400

@app.route("/credentials", methods=["GET"])
def getData():
    correo = request.args.get('correo')
    contrasena = request.args.get('contrasena')

    with connection:
        with connection.cursor() as cursor:
            print("Ejecutando consulta:", cursor.mogrify(GET_CREDENTIALS2.format(correo,contrasena)))
            cursor.execute(GET_CREDENTIALS2.format(correo,contrasena))
            credentials = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]  
    if credentials is not None:
        result = dict(zip(column_names, credentials))
        return jsonify(result)
    else:
        return "Usuario o contraseña erroneos",400


if __name__ == "__main__":
    app.run()