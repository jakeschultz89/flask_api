from flask import Flask, abort, render_template, request
from mock_data import mock_data
from flask_cors import CORS
from config import db, json_parse
import json
from bson import ObjectId

app = Flask(__name__)
CORS(app) #allow anyone to call the server (**DANGER**)


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
    cursor = db.products.find({}) # find with no filter/get all in the collection
    catalog = []
    for prod in cursor:
        catalog.append(prod)

    # investigative HW: read about Python list comprehension

    print(len(catalog), "Records obtained from db" ) 

    return json_parse(catalog) # error

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
    db.products.insert_one(product)

    # return the saved object
    return json_parse(product)


# /api/catagories
@app.route("/api/categories")
def get_categories():
    # return the list (string) of UNIQUE catagories
    categories = []
    # get all the prods from db into a cursor
    cursor = db.products.find({})
    # iterate over the cursor instead of mock_data
    for prod in cursor:
        if not prod["category"] in categories:
            categories.append(prod["category"])

    # logic
    return json_parse(categories)

@app.route("/api/product/<id>")
def get_product(id):
    product = db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return abort(404) # 404 = Not Found
    
    return json_parse(product)

# api/catalog/<category>
# return all the products that belong to that category
@app.route("/api/catalog/<category>")
def get_by_category(category):
    # mongo to search case insensitive we use Regular Expressions
    cursor = db.products.find({"category": category})
    list = []
    for prod in cursor:
        list.append(prod)
    
    return json_parse(list)


# /api/cheapest
@app.route("/api/cheapest")
def get_cheapest():
    cursor = db.products.find({})
    pivot = cursor[0]
    for prod in cursor:
        if prod["price"] < pivot["price"]:
            pivot = prod

        return json_parse(prod)


#################################
######Coupon Codes###############
#################################

# POST to /api/couponcodes
@app.route("/api/couponCodes", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    # validations
    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Code is required and must be at least 5 characters")

    # save
    db.couponCodes.insert_one(coupon)
    return json_parse(coupon)

# GET to /api/couponcodes
@app.route("/api/couponCodes", methods=["GET"])
def get_coupons():
    # read the coupons from db into a cursor
    cursor = db.couponCodes.find({})
    # parse the cursor into a list
    all_coupons = []
    for cp in cursor:
        all_coupons.append(cp)
    # return the list as json
    return json_parse(all_coupons)


# get coupon by its code or 404 if not found
@app.route("/api/couponcodes/<code>")
def get_coupon_by_code(code):
    # get coupon from db
    coupon = db.couponCodes.find_one({"code": code})
    # if not found, return 404
    if coupon is None:
        return abort(404, "Invalid coupon code")
    # otherwise return as JSON
    return json_parse(coupon)

@app.route("/test/onetime/filldb")
def fill_db():
    # iterate over mock_data list
    for prod in mock_data:
        # save every object to db.products
        prod.pop("_id") #remove the _id from the dictionary/product
        db.products.insert_one(prod)

    return "Done!"



# start the server
# debug true will restart the server automatically
app.run(debug=True)