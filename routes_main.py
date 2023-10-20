from flask import Flask, render_template, request, redirect, url_for,Blueprint
import sqlite3,datetime,os
from werkzeug.utils import secure_filename
from . import db_manager as db
from .models import Category,Product,User

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

main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

basedir = os.path.abspath(os.path.dirname(__file__)) 

# Inicio SQLAlchemy

now = datetime.datetime.utcnow

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    sqlite3_database_path = ('database.db')
    con = sqlite3.connect(sqlite3_database_path)
    con.row_factory = sqlite3.Row
    return con


@main_bp.route("/")
def hello_world():
    return render_template('hello.html')

@main_bp.route("/list")
def lista_productes():
    # try:
    #     with get_db_connection() as con:
    #         res = con.execute("SELECT * FROM products")
    #         datos = res.fetchall()
    #     return render_template("products/list.html", elements = datos)
    # except Exception as e:
    #     return str(e), 500
    datos = db.session.query(Product).all()
    return render_template("products/list.html", datos=datos)
    
@main_bp.route("/products/create", methods = ["GET", "POST"])
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

    # with get_db_connection() as con:
    #     sql = "INSERT INTO products (title, description, photo, price, created, updated) VALUES (?, ?, ?, ?, ?, ?)"
    #     con.execute(sql, (titulo, descripcion, foto, precio, created, updated))
    #     con.commit()
    #     # con.close()

    producte_nou = Product()
    producte_nou.title = titulo 
    producte_nou.description = descripcion
    producte_nou.photo = foto
    producte_nou.price = precio
    producte_nou.category_id = 1
    producte_nou.seller_id = 1
    producte_nou.created = created
    producte_nou.updated = updated

    db.session.add(producte_nou)
    db.session.commit()

    return redirect(url_for("main_bp.lista_productes"))
    # except:
    #     return("Error al crear el producte")

@main_bp.route("/products/update/<int:product_id>", methods = ["GET", "POST"])
def modificar_producte(product_id):
    producte = db.session.query(Product).filter(Product.id == product_id).one()

    if request.method == 'GET':
        datos = db.session.query(Product).filter(Product.id == product_id).one()
        app.logger.info(datos)
        return render_template("products/update.html", datos=datos)
    else:
        titol = request.form['titulo']
        desc = request.form['descripcion']
        foto = request.files['foto'].filename
        archivo =request.files['foto']
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        precio = float(request.form['precio'])

        producte.title = titol
        producte.description = desc
        producte.photo = foto
        producte.price = precio

        db.session.add(producte)
        db.session.commit()

        return redirect(url_for('main_bp.lista_productes'))
    
@main_bp.route("/products/delete/<int:product_id>", methods=["GET"])
def eliminar_producte(product_id):
    producte = db.session.query(Product).filter(Product.id == product_id).first()
    if producte:
        db.session.delete(producte)
        db.session.commit()
    return redirect(url_for("main_bp.lista_productes"))

@main_bp.route("/products/read/<int:product_id>")
def ver_producte(product_id):
    producte = db.session.query(Product).filter(Product.id == product_id).one()
    return render_template("products/read.html", producte=producte)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

