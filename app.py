from logging import debug
from flask import Flask, render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user_enquery.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product_lists.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserEnquery(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(25) , nullable= False)
    email = db.Column(db.String(30) , nullable = False)
    Enquery = db.Column(db.String(500) , nullable = False)
    date = db.Column(db.DateTime , default=datetime.utcnow )

    #repr fn is used to show what you want to see from db
    #in cmd use ->python-> from app import db -> db.create_all() to export db on folder
    def __repr__(self) -> str:
        return f"{self.name} -- {self.email} -- {self.Enquery}"


class ProductList(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    productId = db.Column(db.String(10) , nullable = False)
    productName = db.Column(db.String(200) , nullable = False)
    productDescription = db.Column(db.String(5000) , nullable = False)
    productPrice = db.Column(db.Integer , nullable = False)
    date_added = db.Column(db.DateTime ,default = datetime.utcnow, nullable = False)


    def __repr__(self) -> str:
        return f"{self.productId} -- {self.productName} -- {self.productDescription} -- {self.productPrice}"


@app.route("/")
def home_page():
    allProduct = ProductList.query.all()

    return render_template("index.html" , allProduct = allProduct)


@app.route("/blogs")
def blogs():
    return render_template("blog.html")

# random string generator
def product_id_generator(size=10, chars=string.ascii_lowercase + string.digits):
     return ''.join(random.choice(chars) for _ in range(size))


@app.route("/products", methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        productName = request.form['productName']
        productDescription = request.form['productDesc']
        productPrice = request.form['productPrice']
        product_id = product_id_generator()
        print("post")
        product_list = ProductList(productId = product_id , productName = productName , productDescription= productDescription,
        productPrice = productPrice)
        db.session.add(product_list)
        db.session.commit()
    allProducts = ProductList.query.all()
    return render_template("products.html" , allProducts = allProducts)


@app.route("/update/<int:sno>" , methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        productName = request.form['productName']
        productDescription = request.form['productDesc']
        productPrice = request.form['productPrice'] 
        updateProduct= ProductList.query.filter_by(sno = sno).first()
        updateProduct.productName = productName
        updateProduct.productDescription = productDescription
        updateProduct.productPrice = productPrice
        db.session.add(updateProduct)
        db.session.commit()
        return redirect('/products')

    updateProduct = ProductList.query.filter_by(sno = sno).first()
    return render_template("update.html" , updateProduct = updateProduct)


@app.route("/delete/<int:sno>")
def delete(sno):
    product = ProductList.query.filter_by(sno = sno).first()
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')


@app.route("/contact-us")
def contact():
    contact_us = UserEnquery(name = "Amit" , email = "amitanand9799@gmail.com" , Enquery = "You are learning well")
    db.session.add(contact_us)
    db.session.commit()
    return render_template("contactUs.html")



if __name__ == "__main__":
    app.run(debug=True)