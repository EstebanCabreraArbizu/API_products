from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash
password = 'ZeroAutomata03!'
# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = 'computer_products'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', products=data)


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        unit_price = request.form['unit_price']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO products (name,description,category,unit_price,stock) VALUES (%s,%s,%s,%s,%s)",
            (name, description, category, unit_price, stock)
        )
        mysql.connection.commit()
        cur.close()
        flash('Product Added Successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_product(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products WHERE id_products = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-product.html', product=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        unit_price = request.form['unit_price']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE products
            SET name = %s,
                description = %s,
                category = %s,
                unit_price = %s,
                stock = %s
            WHERE id_products = %s
        """, (name, description, category, unit_price, stock, id))
        flash('Product Updated Successfully')
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_product(id):
    cur = mysql.connection.cursor()
    print(id)
    cur.execute('DELETE FROM products WHERE id_products = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    flash('Product Removed Successfully')
    return redirect(url_for('Index'))


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
