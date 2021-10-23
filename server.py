from flask import Flask, abort, render_template, request
from mock_data import mock_data
import json

app = Flask(__name__)
coupon_codes = [
    {
        "code": "qwerty",
        "discount": 10
    }
]

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

@app.route("/api/catalog", methods=["get"])
def get_catalog():
    # returns the catalog JSON
    return json.dumps(mock_data)

@app.route("/api/catalog", methods=["post"])
def save_product():
    # get request payload/body
    product = request.get_json()

    # data validation
    # 1 title exist and is longer than 5 characters

    # validate that title exists in the dictionary and if not then abort (400)
    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title is required and should be at least 5 characters") # 400 = bad request

    print(product["price"])

    # validate that price exists and is greater than 0

    if not 'price' in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should a valid number")

    if product['price'] <= 0:
        return abort(400,"Price should be greater than 0")

    # save the product
    mock_data.append(product)
    product["_id"] = len(product["title"])

    # return the saved object
    return json.dumps(product)


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


#################################
######Coupon Codes###############
#################################

# POST to /api/couponcodes
@app.route("api/couponcodes")
def save_coupon():
    coupon = request.get_json()

    # validations

    # save
    coupon_codes.append(coupon)
    coupon["_id"] = len(coupon["code"])
    return json.dumps(coupon)

# GET to /api/couponcodes
@app.route("/api/couponcodes")
def get_coupons():
    return json.dumps(coupon_codes)


# get coupon by its code or 404 if not found
@app.route("/api/couponcodes/<code>")
def get_coupon_by_code(code):
    for coupon in coupon_codes:
        if(coupon["code"] == code):
            return json.dumps(coupon)

    return abort(404)

# start the server
# debug true will restart the server automatically
app.run(debug=True)