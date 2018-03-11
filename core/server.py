#!/bin/python3
#author: matthew smith mrs9107
#file: server_new.py
#purpose: to move past that janky http server and move to flask

from flask import Flask, Response, request
from database_manager import dbm
from bson import objectid
from bson.json_util import dumps
from config import *
import sys
import hashlib

app =  Flask("ACF")

resp200 = Response({"status": "200 OK"}, status = 200, mimetype='application/json')
resp501 = Response({"status": "501"}, status = 501, mimetype='application/json')

rfid_command_queue = None

_DEBUG = False

#pet(pet name)
#flask endpoint for dealing with pets via name
#capitalizations matter--[SMELL]
@app.route('/pets/name/<pet_name>', methods = ['GET', 'POST', 'DELETE'])
def pet(pet_name):
    db = dbm().db
    pets = dbm().pets
    resp = resp501
    if request.method == 'GET':
        if pets.find({"name":pet_name}).count() > 0:
            data = pets.find_one({"name":pet_name})
            print(data, file=sys.stderr)
            js = dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            #http://blog.luisrei.com/articles/flaskrest.html

    elif request.method == 'POST':
        #this string split is sketchy [SMELL]
        if request.headers['Content-Type'][:16] == 'application/json':
            #check name if already in db, if so
            #run a replace with updated pet info
            #else create new pet in db
            if _DEBUG:
                print("it's a json")
                raw_data = request.get_data()
                print(raw_data)

            data = request.json

            if pets.find({"name":pet_name}).count() > 0:
                print("we're updating stuff")
                #no data cleansing. Maybe should do more
                pets.update_one({"name":pet_name}, {"$set":data})

            else:
                print("we're adding stuff")
                print(data, file=sys.stderr)
                pets.insert_one(data)

            #badly assuming inserts went well
            resp = resp200
        else:
            print("POST failed: body of non-JSON type")
            resp = resp501

    elif request.method == 'DELETE':
        #you heard the man
        delete_count = pets.delete_many({"name":pet_name})
        print("{} entries deleted\n".format(delete_count))
        if delete_count > 0:
            resp = resp200
        else:
            resp = resp501
    else:
        #error 501
        resp = resp501
        pass
    return resp


@app.route('/sfeeder/config', methods = ['GET','POST'])
def feeder_config():
    feeders = dbm().feeders
    resp = resp501
    if request.method == 'GET':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            if feeders.find(data).count() > 0:
                print(data, file=sys.stderr)
                resp = Response(dumps({'bool':True}), status=200, mimetype='application/json')
            else :
                resp = Response(dumps({'bool':False}), status=200, mimetype='application/json')

    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            if data['key'] == "CanIHasCheezeburger":
                #attempt at hashing to make a key but http requests don't like binary values
                #sha = hashlib.sha256()
                print(data, file=sys.stderr)

                ip = request.environ['REMOTE_ADDR']

                #sha.update(data['id'])
                #newkey = str(sha.digest())
                newkey = str(data['id'] * 31)
                feeder_js = {"id":data['id'], "key":newkey, "ip":ip}

                if feeders.find({"id":data['id']}).count() > 0:
                    feeders.update_one({"id":data['id']},{"$set":feeder_js})
                else:
                    feeders.insert_one(feeder_js)

                resp_js_str = dumps({"bool":True, "key":newkey})
            else:
                resp_js_str = dumps({"bool":False, "key":""})

            resp = Response(resp_js_str, status = 200, mimetype = 'application/json')

    return resp

#be able to get data on all pets in order to initalize local data or update local data
@app.route('/pets/', methods = ['GET'])
def get_all_pets():
    db = dbm().db
    pets = dbm().pets

    if request.method == 'GET':
        #return all pets
        pet_cursor = pets.find({})
        if len(pet_cursor) > 0:
            for document in pet_cursor:
                data += document
            js = dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
        else:
            resp = resp501

    else:
        resp = resp501

    return resp

@app.route('/pets/id/<pet_id>', methods = ['GET', 'POST', 'DELETE'])
def pet_by_id(pet_id):
    db = dbm()
    #yada yada


#for shabab to ping the server
@app.route('/', methods = ['GET'])
def hello_server():
    if request.method == 'GET':
        return resp200


def run_server(queue):
    app.run(host='0.0.0.0')
    rfid_command_queue = queue

if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=False)#runs on all local interfaces
    run_server()
