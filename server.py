from flask import Flask

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
    return "Hello from a Flask Server"

@app.route("/test")
def test():
    return "Hello there!"

@app.route("/about")
def about():
    return me["name"] + " " + me["last"]

@app.route("/address")
def address():
    return me["address"]

@app.route("/email")
def email():
    return me["email"]

# start the server
# debug true will restart the server automatically
app.run()