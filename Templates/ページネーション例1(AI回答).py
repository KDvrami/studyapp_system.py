from flask import Flask, render_template, request
from peewee import SqliteDatabase, Model, IntegerField, TextField

# Initialize Flask app
app = Flask(__name__)

# Initialize Peewee database
db = SqliteDatabase('database.db')

# Define Peewee model
class Item(Model):
    id = IntegerField(primary_key=True)
    name = TextField()

    class Meta:
        database = db

# Create the table and add sample data
db.connect()
db.create_tables([Item])

# Add sample data if table is empty
if Item.select().count() == 0:
    for i in range(1, 101):  # Add 100 items
        Item.create(id=i, name=f'Item {i}')

# Define route with pagination
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    items = Item.select().paginate(page, per_page)
    total_count = Item.select().count()
    total_pages = (total_count + per_page - 1) // per_page

    return render_template('index.html', items=items, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
