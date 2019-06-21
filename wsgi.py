from flask import Flask, request, render_template 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
import os
import logging
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product

admin = Admin(app, template_mode='bootstrap2')
admin.add_view(ModelView(Product, db.session))
@app.route('/hello')
def hello():
   return "Hello World!"

from schemas import products_schema
@app.route('/products')
def get_products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

from schemas import product_schema
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.query(Product).get(id) # SQLAlchemy request => 'SELECT * FROM products'
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def del_product(id):
    try:
       product = db.session.query(Product).get(id)
    except:
       return "", 400    
    db.session.delete(product) # SQLAlchemy request => 'SELECT * FROM products'
    db.session.commit()
    return "", 204

@app.route('/product', methods=['POST'])
def create_product():
    #pdb.set_trace()
    data = request.get_json()['name']
    objProduct = Product()
    objProduct.name = data
    db.session.add(objProduct)
    db.session.commit()
    return "", 201

@app.route('/product/<int:id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()['name']
    try:
       product = db.session.query(Product).get_or_404(id)
    except:
       return "", 400  
    try:
        setattr(product, 'name', request.get_json()['name'])
    except KeyError:
        pass
    db.session.commit()
    return "", 201

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)
