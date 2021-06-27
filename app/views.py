from flask.helpers import send_file
from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
from os import listdir
import json

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
        if product.product_name == "none":
            return render_template('extract_no_product.html.jinja')
        product.save_to_json()
        product.json_info_file()
        return redirect(url_for('opinions', product_id=product_id))
    return render_template('extract.html.jinja')


@app.route('/products')
def products():
    products_list = [product.split('.')[0] for product in listdir("app/products")]
    info = {}
    for file in listdir("app/info"):
        with open(f"app/info/{file}", "r", encoding="UTF-8") as fp:
            f = json.load(fp)
            info[f["id"]] = f
    return render_template('products.html.jinja', info=info, products=products_list)

@app.route('/opinions/<product_id>')
def opinions(product_id):
    print(product_id)
    product = Product(product_id)
    info = {}
    with open(f"app/info/{product_id}_info.json", "r", encoding="UTF-8") as fp:
            r = json.load(fp)
            info = r
    print(", ".join(op.opinion_id for op in product.opinions))
    product.read_from_json()
    return render_template('opinions.html.jinja', info=info, product=str(product))

@app.route('/charts/<productId>')
def charts(product_id):
    pass

@app.route('/about')
def about():
    return render_template('about.html.jinja')

# @app.route('/download/<file_name>')
# def download_json(file_name):
#     path = app.root_path + "/products/" + file_name + ".json"
#     return send_file(path, as_attachment=True)