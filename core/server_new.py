#author: matthew smith mrs9107
#file: server_new.py
#purpose: to move past that janky http server and move to flask

from flask import Flask
from database_manager import dbm
from bson import objectid
from config import *


app =  Flask("ACF")



@app.route('/pets/name/<pet_name>', methods = ['GET', 'POST', 'DELETE'])
def pet(pet_name):
    db = dbm().db
    pets = dbm().pets

    if request.method == 'GET':
        if pets.find({"name":pet_name}).size() > 0:
            data = pets.find_one({"name":pet_name})
            js = jsbon.dumps(data)
            resp = app.Response(js, status=200, mimetype='application/json')
            return resp
            #http://blog.luisrei.com/articles/flaskrest.html

    elif request.method == 'POST':
        #data = request.form
        if request.headers['Content-Type'] == 'application/json':
            #check name if already in db, if so
            #run a replace with updated pet info
            #else create new pet in db
            data = request.form
            if pets.find({"name":pet_name}).size > 0:
                #replace?
                pass
            else:
                #create new guy
                pass

        else:
            #fug off with that other stuff
    elif request.method == 'DELETE':
        #you heard the man

    else:
        #error

@app.route('/pets/id/<pet_id>', methods = ['GET', 'POST', 'DELETE'])
def pet_by_id(pet_id):
    db = dbm()
    #yada yada



if __name__ == "__main__":
    app.run(host+port)
