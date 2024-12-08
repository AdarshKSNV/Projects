from flask import Flask, render_template, request, redirect, url_for, flash
import os
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="wish_vault"
)
cursor = db.cursor()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("INSERT INTO wishlist (title, description) VALUES (%s, %s)", (title, description))
        db.commit()
        flash('Wishlist item added successfully!')
    cursor.execute("SELECT * FROM wishlist")
    items = cursor.fetchall()
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/delete/<int:id>')
def delete_wishlist(id):
    cursor.execute("DELETE FROM wishlist WHERE id=%s", (id,))
    db.commit()
    flash('Wishlist item deleted successfully!')
    return redirect(url_for('wishlist'))

@app.route('/memories/<int:wishlist_id>', methods=['GET', 'POST'])
def memories(wishlist_id):
    if request.method == 'POST':
        file = request.files['image']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            cursor.execute("INSERT INTO memories (wishlist_id, image_path) VALUES (%s, %s)", (wishlist_id, file_path))
            db.commit()
            flash('Memory added successfully!')
    cursor.execute("SELECT * FROM memories WHERE wishlist_id=%s", (wishlist_id,))
    images = cursor.fetchall()
    return render_template('memories.html', images=images, wishlist_id=wishlist_id)

@app.route('/favorites')
def favorites():
    cursor.execute("SELECT * FROM memories WHERE is_favorite=TRUE")
    favorites = cursor.fetchall()
    return render_template('favorites.html', favorites=favorites)

@app.route('/mark_favorite/<int:id>')
def mark_favorite(id):
    cursor.execute("UPDATE memories SET is_favorite=TRUE WHERE id=%s", (id,))
    db.commit()
    flash('Marked as favorite!')
    return redirect(url_for('favorites'))

if __name__ == '__main__':
    app.run(debug=True)
