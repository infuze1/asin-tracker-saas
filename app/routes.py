# filepath: app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models import db, Product
from app.utils import get_amazon_product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print(f"Current app: {current_app}")  # Debug: Check if app context is active
    products = Product.query.all()  # Query the Product table
    return render_template('index.html', products=products)

@main.route('/track', methods=['POST'])
def track():
    asin = request.form.get('asin')
    threshold = request.form.get('threshold')
    user_id = 1  # Replace with actual user authentication logic

    product_data = get_amazon_product(asin)
    if product_data:
        product = Product(
            asin=asin,
            user_id=user_id,
            price=product_data['price'],
            threshold=threshold
        )
        db.session.add(product)
        db.session.commit()
        flash(f"Tracking {product_data['title']} at £{product_data['price']}", 'success')
    else:
        flash("Failed to retrieve product information. Please check the ASIN.", 'danger')

    return redirect(url_for('main.index'))

@main.route('/remove/<int:product_id>', methods=['POST'])
def remove(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash("Product removed successfully.", 'success')
    else:
        flash("Product not found.", 'danger')

    return redirect(url_for('main.index'))