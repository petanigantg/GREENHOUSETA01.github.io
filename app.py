#from re import S
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort, make_response, send_file
import bcrypt
import base64
from pymongo import MongoClient
import array as arr
import gridfs
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = "%^^^greenhouse06^^^AT123>...<"
myclient = MongoClient("mongodb+srv://greenhouse06:peAELSBNORDyW6iC@cluster0.ikrjp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["record"]
mycol2 = mydb["user"]

sidebarON = 0

def notification():
    notifEC = 0
    ECword = ""
    buttonCON=mydb.button.find_one()
    dataACTUAL=mydb.actual.find_one()
    EClimitATAS = buttonCON["EClimitATAS"]
    EClimitBAWAH = buttonCON["EClimitBAWAH"]
    PHlimitATAS = buttonCON["PHlimitATAS"]
    PHlimitBAWAH = buttonCON["PHlimitBAWAH"]
    KELEMBAPANlimitATAS = buttonCON["KELEMBAPANlimitATAS"]
    KELEMBAPANlimitBAWAH = buttonCON["KELEMBAPANlimitBAWAH"]

    #Cek Notif nilai EC
    if float(dataACTUAL["EC"]) > EClimitATAS:
        notifEC = 1
        ECword = "Nilai EC melebihi Batas Maksimal"
    elif float(dataACTUAL["EC"]) < EClimitBAWAH:
        notifEC = 1
        ECword = "Nilai EC Kurang dari Batas Minimum"
    else:
        notif = 0

    #Cek Notif nilai pH
    if float(dataACTUAL["PH"]) > PHlimitATAS:
        notifPH = 1
        PHword = "Nilai pH melebihi Batas Maksimal"
    elif float(dataACTUAL["PH"]) < PHlimitBAWAH:
        notifPH = 1
        PHword = "Nilai pH Kurang dari Batas Minimum"
    else:
        notifPH = 0
    
    #Cek Notif nilai KELEMBAPAN
    if float(dataACTUAL["KELEMBAPAN"]) > KELEMBAPANlimitATAS:
        notifKELEMBAPAN = 1
        KELEMBAPANword = "Nilai Kelembapan melebihi Batas Maksimal"
    elif float(dataACTUAL["KELEMBAPAN"]) < KELEMBAPANlimitBAWAH:
        notifKELEMBAPAN = 1
        KELEMBAPANword = "Nilai Kelembapan Kurang dari Batas Minimum"
    else:
        notifKELEMBAPAN = 0
    
    notif = (notifEC, ECword, notifPH, PHword, notifKELEMBAPAN, KELEMBAPANword)
    return notif


def getimage():
    fs = gridfs.GridFS(mydb)
    name = 'picture.jpg'
    download = "static/img/" + name
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

@app.route('/EClimit', methods=['GET', 'POST'])
def EClimit():
        EClimitATAS = request.form['EClimitATAS']
        EClimitBAWAH = request.form['EClimitBAWAH']
        myquery = { "_id": 1 }
        newvalues = { "$set": {"EClimitATAS": float(EClimitATAS) , "EClimitBAWAH" : float(EClimitBAWAH)} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/PHlimit',  methods=['GET', 'POST'])
def PHlimit():
        PHlimitATAS = request.form['PHlimitATAS']
        PHlimitBAWAH = request.form['PHlimitBAWAH']
        myquery = { "_id": 1 }
        newvalues = { "$set": {"PHlimitATAS": float(PHlimitATAS) , "PHlimitBAWAH" : float(PHlimitBAWAH)} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/KELEMBAPANlimit',  methods=['GET', 'POST'])
def KELEMBAPANlimit():
        KELEMBAPANlimitATAS = request.form['KELEMBAPANlimitATAS']
        KELEMBAPANlimitBAWAH = request.form['KELEMBAPANlimitBAWAH']
        myquery = { "_id": 1 }
        newvalues = { "$set": {"KELEMBAPANlimitATAS": float(KELEMBAPANlimitATAS) , "KELEMBAPANlimitBAWAH" : float(KELEMBAPANlimitBAWAH)} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))


@app.route('/refreshFOTO')
def refreshFOTO():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"CAMERA": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('home'))

@app.route('/autoON')
def controlAUTOon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"PAUSE": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/autoOFF')
def controlAUTOoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"PAUSE": 0} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/notifON')
def controlNOTIFon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"sistemnotifikasi": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/notifOFF')
def controlNOTIFoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"sistemnotifikasi": 0} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))


@app.route('/kipasON')
def controlKIPASon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"KIPAS": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/kipasOFF')
def controlKIPASoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"KIPAS": 0} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/lampuON')
def controlLAMPUon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"LAMPU": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/lampuOFF')
def controlLAMPUoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"LAMPU": 0} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/pompaON')
def controlPOMPAon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"POMPA": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/pompaOFF')
def controlPOMPAoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"POMPA": 0} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/humidifierON')
def controlHUMIDIFIERon():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"HUMIDIFIER": 1} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/humidifierOFF')
def controlHUMIDIFIERoff():
        myquery = { "_id": 1 }
        newvalues = { "$set": {"HUMIDIFIER": 0} }
        mydb.button.update_one(myquery, newvalues)
        return redirect(url_for('control'))

@app.route('/excelDownload')
def excelDownload():
    dataRECORD = list(mydb.record.find())
    data = pd.DataFrame(dataRECORD)
    data.to_excel('GreenHouse06Record.xlsx', sheet_name='sheet1', index=False)
    path = "static\\filerecord\\GreenHouseRecord.xlsx"
    return send_file(path, as_attachment=True)

@app.route('/')
def home():
    sidebarON = 1
    notif = notification()
    dataACTUAL=mydb.actual.find_one()
    getimage()
    foto = mydb.button.find_one()
    return render_template("index.html",  foto=foto, dataACTUAL=dataACTUAL, notif=notif, sidebarON=sidebarON)
    
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
                return redirect(url_for('home'))
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
    sidebarON = 5
    notif = notification()
    return render_template("blank.html", notif=notif, sidebarON=sidebarON)

@app.route('/control', methods=["GET", "POST"])
def control():
    sidebarON = 4
    if session:
        buttonCON=mydb.button.find_one()
        kipasCON=buttonCON["KIPAS"]
        lampuCON=buttonCON["LAMPU"]
        pompaCON=buttonCON["POMPA"]
        humidifierCON=buttonCON["HUMIDIFIER"]
        dataLIMIT = mydb.button.find_one()
        notif = notification()
        return render_template("control.html", kipasCON=kipasCON,lampuCON=lampuCON,pompaCON=pompaCON,humidifierCON=humidifierCON,dataLIMIT=dataLIMIT, notif=notif, sidebarON=sidebarON)
    else:
        return redirect(url_for('login'))

@app.route('/docs', methods=["GET", "POST"])
def docs():
    sidebarON = 3
    dataRECORD = list(mydb.record.find())
    notif = notification()
    return render_template("tables.html", dataRECORD=dataRECORD, notif=notif, sidebarON=sidebarON)

@app.route('/grafik', methods=["GET", "POST"])
def grafik():
    sidebarON = 2
    notif = notification()
    dataGRAFIK = list(mydb.grafik_data.find().sort("_id"))
    return render_template("charts.html", dataGRAFIK=dataGRAFIK, notif=notif, sidebarON=sidebarON)

@app.route('/LCD')
def homeLCD():
    session['firstname'] = "LCD"
    session['lastname'] = "Account"
    session['email'] = ""
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)