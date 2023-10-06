from flask import Flask, request, render_template, redirect, url_for, g
import sqlite3, os
from werkzeug.utils import secure_filename
import datetime

DATABASE = 'database.db'
UPLOAD_FOLDER = "upload"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    sqlite3_database_path = ('database.db')
    con = sqlite3.connect(sqlite3_database_path)
    con.row_factory = sqlite3.Row
    return con


@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/list")
def lista_productes():
    try:
        with get_db_connection() as con:
            res = con.execute("SELECT * FROM products")
            datos = res.fetchall()
        return render_template("products/list.html", elements = datos)
    except Exception as e:
        return str(e), 500
    
@app.route("/products/create", methods = ["GET", "POST"])
def crear_productes():
    # try:
    if request.method == 'GET':
        return render_template('/products/create.html')
    elif request.method == 'POST':
        dades = request.form
        titulo = dades.get("titulo")
        descripcion = dades.get("descripcion")
        foto = request.files['foto'].filename
        precio = int(dades.get("precio"))
        created = datetime.datetime.now()
        updated = datetime.datetime.now()
        archivo =request.files['foto']
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    with get_db_connection() as con:
        sql = "INSERT INTO products (title, description, photo, price, created, updated) VALUES (?, ?, ?, ?, ?, ?)"
        con.execute(sql, (titulo, descripcion, foto, precio, created, updated))
        con.commit()
        # con.close()
    return redirect(url_for("lista_productes"))
    # except:
    #     return("Error al crear el producte")
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)