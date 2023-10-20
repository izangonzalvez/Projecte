from flask import Flask, request, render_template, redirect, url_for, g
import sqlite3, os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import datetime
# from datetime import datetime

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

basedir = os.path.abspath(os.path.dirname(__file__)) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/database.db"
app.config["SQLALCHEMY_ECHO"] = True

# Inicio SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
now = datetime.datetime.utcnow

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    slug = db.Column(db.Text, nullable=False, unique=True)

# class ConfirmedOrder(db.Model):
#     __tablename__ = "confirmed_orders"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
#     created = db.Column(db.DateTime, default=now)

# class Order(db.Model):
#     __tablename__ = "orders"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
#     buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     created = db.Column(db.DateTime, default=now)
#     UniqueConstraint("products.id","users.id", name="uc_product_buyer")

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created = db.Column(db.DateTime, default=now)
    updated = db.Column(db.DateTime, default=now)

# class SQLiteSequence(db.Model):
#     __tablename__ = "sqlite_sequence"
#     name = db.Column(db.Text, nullable=False, primary_key=True)
#     seq = db.Column(db.Text, nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=now)
    updated = db.Column(db.DateTime, default=now)

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
    # try:
    #     with get_db_connection() as con:
    #         res = con.execute("SELECT * FROM products")
    #         datos = res.fetchall()
    #     return render_template("products/list.html", elements = datos)
    # except Exception as e:
    #     return str(e), 500
    datos = db.session.query(Product).all()
    return render_template("products/list.html", datos=datos)
    
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

    return redirect(url_for("lista_productes"))
    # except:
    #     return("Error al crear el producte")

@app.route("/products/update/<int:product_id>", methods = ["GET", "POST"])
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

        return redirect(url_for('lista_productes'))
    
@app.route("/products/delete/<int:product_id>", methods=["GET"])
def eliminar_producte(product_id):
    producte = db.session.query(Product).filter(Product.id == product_id).first()
    if producte:
        db.session.delete(producte)
        db.session.commit()
    return redirect(url_for("lista_productes"))

@app.route("/products/read/<int:product_id>")
def ver_producte(product_id):
    producte = db.session.query(Product).filter(Product.id == product_id).one()
    return render_template("products/read.html", producte=producte)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)