from flask import Flask,render_template, redirect, url_for, request
import mysql.connector
import numpy as np
from numpy import genfromtxt
from sklearn import linear_model

lr = linear_model.LogisticRegression()
dic={}
val=''





app = Flask(__name__)


@app.route("/about")
def login():
    return render_template("about.html")    

@app.route("/contact")
def contact():
    return render_template("contact.html")    

@app.route('/')
def helloo6():
    return render_template('checksymptom.html')

@app.route("/code",methods=["POST"])
def save():
    conn=mysql.connector.connect(host="localhost",user="root",password="root",database="ex1")
    cur=conn.cursor()
    nam=str(request.form["name"])
    em=str(request.form["email"])
    date=str(request.form["date"])
    general=str(request.form["general"])
    number=str(request.form["number"])
    des=str(request.form["des"])
    cur.execute("insert into checksymptom(name,email,date,general,number,des) values('"+nam+"','"+em+"','"+date+"','"+general+"','"+number+"','"+des+"')")
    conn.commit()
    return "data saved"

@app.route('/Symptoms',methods=['POST'])
def helloo_aapp():
    Max=str(request.form["max"])
    Min=str(request.form["min"])
    Pulse=str(request.form["pulse"])
    Fever=str(request.form["fever"])
    Cold=str(request.form["cold"])
    Disease=str(request.form["disease"])

    conn=mysql.connector.connect(host="localhost",user="root",password="",db="ex1")
    cursor=conn.cursor()
    cursor.execute("insert into add_sym(maxim,minim,pulse,fever,cold,disease)values('"+Max+"','"+Min+"','"+Pulse+"','"+Fever+"','"+Cold+"','"+Disease+"') ")
    conn.commit()

    import csv

    csvData = [(Max, Min, Pulse, Cold, Fever, Disease)]
    with open('hospital.csv', 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()

    return render_template('Symptoms.html')



@app.route('/datatrain')
def datatrain():
    print("hi")
    file=(genfromtxt("hospital.csv",delimiter=',',dtype='str'))
    global lr
    global dic

    count=0
    for val in file:
        if val [5] not in dic:
            dic[val[5]]=count
            count+=1

    for val in file:
        val[5]=dic[val[5]]

    print(file)


    trainingset=file
    testingset=file[1:]

    trainingx=trainingset[:,[0,1,2,3,4]]
   # trainingx=trainingx.astype(float)
    trainingy=trainingset[:,[5]]
    lr.fit(trainingx, trainingy)
    return ('hello')

@app.route('/final',methods=["POST"])
def checkpge1():
    print("hi")
    lis = []
    lis.insert(0, int(request.form["max"]))
    lis.insert(1, int(request.form["min"]))
    lis.insert(2, int(request.form["pulse"]))
    lis.insert(3, int(request.form["cold"]))
    lis.insert(4, int(request.form["fever"]))
    datatrain()
    global lr
    global dic
    a = int(lr.predict([lis]))
    global val
    z=0
    for x in dic:
        if(dic[x] == a):

            print("you might be suffering from %s" %x)
            z=x


    return render_template('finalresult.html',val1=z)





if __name__ == '__main__':
    app.run()
