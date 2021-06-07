from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
from os import listdir

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product(product_id)
        product.extract_product()
        product.save_to_json()
        return redirect(url_for('opinions', product_id=product_id))
    return render_template('extract.html.jinja')


@app.route('/products')
def products():
    products_list = [product.split('.')[0] for product in listdir("app/products")]
    return render_template('products.html.jinja', products=products_list)

@app.route('/opinions/<product_id>')
def opinions(product_id):
    print(product_id)
    product = Product(product_id)
    print(", ".join(op.opinion_id for op in product.opinions))
    product.read_from_json()
    return render_template('opinions.html.jinja', product=str(product))

@app.route('/charts/<productId>')
def charts(product_id):
    pass

@app.route('/about')
def about():
    return render_template('about.html.jinja')
