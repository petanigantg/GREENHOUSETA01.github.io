#from re import S
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort, make_response
import bcrypt
import base64
from pymongo import MongoClient
import array as arr
import gridfs
import json

app = Flask(__name__)
myclient = MongoClient("mongodb+srv://greenhouse06:peAELSBNORDyW6iC@cluster0.ikrjp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["record"]
mycol2 = mydb["user"]


def getimage():
    fs = gridfs.GridFS(mydb)
    name = 'picture.jpg'
    download = "static/image/" + name
    data = mydb.fs.files.find_one({'filename': name })
    my_id = data['_id']
    outputdata = fs.get(my_id).read()
    output = open(download, "wb")
    output.write(outputdata)
    output.close()
"""
@app.route('/lampuON')
def controlLAMPUon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"LAMPU": 1} }
        mydb.button.update_one(myquery, newvalues)
        buttonCON=mydb.button.find_one()
        kipasCON=buttonCON["KIPAS"]
        lampuCON=buttonCON["LAMPU"]
        pompaCON=buttonCON["POMPA"]
        humidifierCON=buttonCON["HUMIDIFIER"]
        return render_template("control.html", kipasCON=kipasCON,lampuCON=lampuCON,pompaCON=pompaCON,humidifierCON=humidifierCON )
"""

@app.route('/kipasON')
def controlKIPASon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"KIPAS": 1} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")


@app.route('/kipasOFF')
def controlKIPASoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"KIPAS": 0} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")

@app.route('/lampuON')
def controlLAMPUon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"LAMPU": 1} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")

@app.route('/lampuOFF')
def controlLAMPUoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"LAMPU": 0} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")

@app.route('/pompaON')
def controlPOMPAon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"POMPA": 1} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")

@app.route('/pompaOFF')
def controlPOMPAoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"POMPA": 0} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")

@app.route('/humidifierON')
def controlHUMIDIFIERon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"HUMIDIFIER": 1} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")

@app.route('/humidifierOFF')
def controlHUMIDIFIERoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"HUMIDIFIER": 0} }
        mydb.button.update_one(myquery, newvalues)
        return render_template("control.html")





@app.route('/')
def home():
        dataACTUAL=mydb.actual.find_one()
        getimage()

        dataRECORD = list(mydb.record.find())

        return render_template("index.html",  dataRECORD=dataRECORD, dataACTUAL=dataACTUAL)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.clear()
        details = request.form
        email = details['email']
        password = details['password'].encode('utf-8')
        cekemail = {"email": email }
        user = mycol2.find_one(cekemail)
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        if user:
            if bcrypt.hashpw(password, user["password"]) == user["password"]:
            #if bcrypt.hashpw(password, bcrypt.gensalt()) == user["password"]:
                session['firstname'] = user['firstname']
                session['lastname'] = user['lastname']
                session['email'] = user['email']
                LogCondition = True
                return redirect(url_for('control'))
            else:
                flash('User and password not match!')
                return render_template("login.html")
        else:
            flash('User not found!')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        #hash_password = bcrypt.generate_password_hash(password)
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        inUSER =  [{ "firstname": firstname, "lastname": lastname, "email": email, "password": bcrypt.hashpw(password, bcrypt.gensalt())} ] 
        
        doc = mydb.user.insert_many(inUSER)
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

@app.route('/base', methods=["GET", "POST"])
def base():
    return render_template("blank.html")

@app.route('/control', methods=["GET", "POST"])
def control():
    if session:
        buttonCON=mydb.button.find_one()
        kipasCON=buttonCON["KIPAS"]
        lampuCON=buttonCON["LAMPU"]
        pompaCON=buttonCON["POMPA"]
        humidifierCON=buttonCON["HUMIDIFIER"]
        return render_template("control.html", kipasCON=kipasCON,lampuCON=lampuCON,pompaCON=pompaCON,humidifierCON=humidifierCON )
    else:
        return redirect(url_for('login'))

@app.route('/docs', methods=["GET", "POST"])
def docs():
    dataRECORD = list(mydb.record.find())
    return render_template("tables.html", dataRECORD=dataRECORD)

@app.route('/grafik', methods=["GET", "POST"])
def grafik():
    dataGRAFIK = list(mydb.grafik_data.find().sort("_id"))
    return render_template("charts.html", dataGRAFIK=dataGRAFIK)

if __name__ == '__main__':
    app.secret_key = "%___greenhouse06^^^AT123___>...<"
    app.run(debug=True)