<<<<<<< HEAD
#!/bin/python3
=======
#!/bin/python
>>>>>>> 262ec59f64d87d888fa8a05cf95dfb37d21b9574
#author: matthew smith mrs9107
#file: server_new.py
#purpose: to move past that janky http server and move to flask

from flask import Flask, Response, request
from database_manager import dbm
from bson import objectid
from bson.json_util import dumps
from config import *
import sys

app =  Flask("ACF")

resp200 = Response({"status": "200 OK"}, status = 200, mimetype='application/json')
resp501 = Response({"status": "501"}, status = 501, mimetype='application/json')


@app.route('/pets/name/<pet_name>', methods = ['GET', 'POST', 'DELETE'])
def pet(pet_name):
    db = dbm().db
    pets = dbm().pets

    if request.method == 'GET':
        if pets.find({"name":pet_name}).count() > 0:
            data = pets.find_one({"name":pet_name})
            print(data, file=sys.stderr)
            js = dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            #http://blog.luisrei.com/articles/flaskrest.html

    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            #check name if already in db, if so
            #run a replace with updated pet info
            #else create new pet in db
            data = request.json
            if pets.find({"name":pet_name}).count() > 0:
                #no data cleansing. Maybe should do more
<<<<<<< HEAD
                pets.update_one({"name":pet_name}, data)
=======
                pets.update_one({"name":pet_name}, {"$set":data})
>>>>>>> 262ec59f64d87d888fa8a05cf95dfb37d21b9574
            else:
                print(data, file=sys.stderr)
                pets.insert_one(data)

            #badly assuming inserts went well
            resp = resp200
        else:
            #fug off with that other stuff
            resp = resp501
    elif request.method == 'DELETE':
        #you heard the man
        resp = resp501
    else:
        #error 500
        resp = resp501
        #probably goes against standards, talk about response formats with team
    return resp
@app.route('/pets/id/<pet_id>', methods = ['GET', 'POST', 'DELETE'])
def pet_by_id(pet_id):
    db = dbm()
    #yada yada



if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host='127.0.0.1')
=======
#    app.run(host='127.0.0.1')
    app.run(host='0.0.0.0')
>>>>>>> 262ec59f64d87d888fa8a05cf95dfb37d21b9574
