from flask import Flask, abort, render_template
from mock_data import mock_data
import json

app = Flask(__name__)

me = {
    "name": "Jake",
    "last": "Schultz",
    "age": 31,
    "hobbies":[],
    "address": {
        "street": "Proctor",
        "city": "Akron"
    },
    "email": "ejacobschultz@gmail.com"
}

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route("/test")
def test():
    return "Hello there!"

@app.route("/about")
def about():
    return render_template('about.html')
    # return me["name"] + " " + me["last"]

@app.route("/address")
def address():
    return me["address"]

@app.route("/email")
def email():
    return me["email"]



#########################################
# API Methods
#########################################

@app.route("/api/catalog")
def get_catalog():
    # returns the catalog JSON
    return json.dumps(mock_data)


# /api/catagories
# return the list (string) of UNIQUE catagories
@app.route("/api/categories")
def get_categories():
    categories = []
    for prod in mock_data:
        print(prod["category"])

        if not prod["category"] in categories:
            categories.append(prod["category"])

    return json.dumps(categories)

@app.route("/api/product/<id>")
def get_product(id):
    for prod in mock_data:
        if prod["_id"] == id:
            return prod

    return abort(404) # 404 = not found

# api/catalog/<category>
# return all the products that belong to that category
@app.route("/api/catalog/<category>")
def get_by_category(category):
    result = []
    for prod in mock_data:
        if prod["category"].lower() == category.lower():
            result.append(prod)

    return json.dumps(result)


# /api/cheapest
@app.route("/api/cheapest")
def get_cheapest():
    pivot = mock_data[0]
    for prod in mock_data:
        if prod["price"] < pivot["price"]:
            pivot = prod

    return pivot

# start the server
# debug true will restart the server automatically
app.run(debug=True)