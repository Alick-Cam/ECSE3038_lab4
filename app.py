from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

#adding Profile imports
#adding time stuff
from pytz import datetime
import pytz

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://aivrrkaq:s25O20MPIxzPrquAYgr6eeqhVoLj7R8l@ziggy.db.elephantsql.com:5432/aivrrkaq"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False

#global dictionary to store information about a single user 
userData = {}

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Tank(db.Model):
    __tablename__ = "Tank"

    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String())
    lat = db.Column(db.String())
    long = db.Column(db.String())
    percentage_full = db.Column(db.String())

class TankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tank
        fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/data")
def data_get():
    tanks = Tank.query.all()
    tanks_json = TankSchema(many=True).dump(tanks)
    return jsonify(tanks_json)

@app.route('/data', methods = ["POST"])
def data_post():
    newTank = Tank(
        location = request.json["location"],
        lat = request.json["lat"],
        long = request.json["long"],
        percentage_full = request.json["percentage_full"]
    )
    db.session.add(newTank)
    db.session.commit()
    return TankSchema().dump(newTank)

@app.route('/data/<int:id>', methods = ["PATCH"])
def data_patch(id):
    tank = Tank.query.get(id)
    patch = request.json
    if "location" in patch:
        tank.location = patch["location"]
    if "lat" in patch:
        tank.lat = patch["lat"]
    if "long" in patch:
        tank.long = patch["long"]
    if "percentage_full" in patch:
        tank.percentage_full = patch["percentage_full"]

    db.session.commit()
    return TankSchema().dump(tank)

@app.route('/data/<int:id>', methods = ["DELETE"])
def data_delete(id):
    tank = Tank.query.get(id)
    db.session.delete(tank)
    db.session.commit()

    return {
        "success":True
    }

#Profile  Routes 
@app.route('/profile')
def profile_get():
    global userData
    successDict = {
        "success" :True,
        "data" : userData
    }
    return jsonify(successDict)

@app.route('/profile', methods = ['POST'])
def profile_post():
    #obtain time stamp
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    #obtain json object from the request object
    userD = request.json
    #do the validation 
    if len(userD) > 0:
        #update global dictionary to show that a user has logged in
        global userData
        userData = userD
        #append time stamp to local dictionary and prepare for return
        userD["last_updated"] = tVartoString
        successDict = {
            "successs":True,
            "data": userD
        }
        return jsonify(successDict)
    else:
        return redirect(url_for("profile_get"))

@app.route('/profile', methods = ["PATCH"])
def profile_patch():
    global userData #this global variable will be updated locally
    #obtain time stamp
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    #obtain json object from the request object in a local dictionary
    userD = request.json   
    #user can only patch if the profile has already been created
    #Therefore, check if global dictionary has an element
    if len(userData) > 0:
        #patch global dictionary
        userData = userD
        #append time stamp to local dictionary and prepare for return
        userD["last_updated"] = tVartoString
        successDict = {
        "successs":True,
        "data": userD
        }            
        return jsonify(successDict)
    else:
        return redirect(url_for("profile_get"))

if __name__ == "__main__":
    app.run(debug = True)


