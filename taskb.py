from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd 

app = Flask(__name__)

PATH_TO_DB = 'retail_app.db'

def from_sqlite3(query):
    con = sqlite3.connect(PATH_TO_DB)
    data = pd.read_sql_query(query, con)
    con.close()
    return data 

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Customers page route
@app.route('/customers/')
def customers():
    return render_template('customers.html')

# Add Customer page route
@app.route('/add_customer/', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        customer_first_name = request.form.get('firstname')
        customer_last_name = request.form.get('lastname')
        customer_gender = request.form.get('gender')
        customer_dob = request.form.get('dob')

        try:
            conn = sqlite3.connect(PATH_TO_DB)
            cursor = conn.cursor()

            insert_sql = """
                INSERT INTO customer(customer_first_name, customer_last_name, customer_gender, customer_dob)
                VALUES (?, ?, ?, ?)
                """

            cursor.execute(insert_sql, (customer_first_name, customer_last_name, customer_gender, customer_dob))

            conn.commit()

        except sqlite3.Error as e:
            print(e)
            return render_template('add_customer.html', error="An error occurred.")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect(url_for('home'))

    return render_template('add_customer.html')  

# Products page route
@app.route('/products/')
def products():
    return render_template('products.html')

# Get Product page route
@app.route('/get_product/', methods=['GET', 'POST'])
def get_product():
    if request.method == 'GET':
        return render_template('get_product.html')

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        query = f"SELECT * FROM product WHERE product_id = {product_id}"
        data = from_sqlite3(query)
        if data.empty:
            return render_template('get_product.html', error="Product not found.")
        else:
            product_list = data.to_dict(orient='records')
            return render_template('product_details.html', products=product_list)

    return render_template('get_product.html')

if __name__ == '__main__':
    app.run(debug=True)
