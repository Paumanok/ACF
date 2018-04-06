#!/bin/python3
#author: matthew smith mrs9107
#file: server_new.py
#purpose: to move past that janky http server and move to flask

from flask import Flask, Response, request
from database_manager import dbm
from bson import objectid
from bson.json_util import dumps
import sys
import hashlib
from queue import *
from util import can_pet_feed

app =  Flask("ACF")

resp200 = Response({"status": "200 OK"}, status = 200, mimetype='application/json')
resp501 = Response({"status": "501"}, status = 501, mimetype='application/json')


_DEBUG = False


class server():
    def __init__(self):
        self.rfid_command_queue = None

this_server = server()
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

                newkey = str(data['id'] * 31)
                feeder_id = available_id()
                feeder_js = {"id":feeder_id, "key":newkey, "ip":ip}

                if feeders.find({"key":newkey}).count() > 0:
                    feeders.update_one({"key":newkey},{"$set":feeder_js})
                else:
                    feeders.insert_one(feeder_js)

                resp_js_str = dumps({"bool":True, "key":newkey})
            else:
                resp_js_str = dumps({"bool":False, "key":""})

            resp = Response(resp_js_str, status = 200, mimetype = 'application/json')

    return resp

NULL_WEIGHT = -1
KEY_INVALID = -1
NO_FEED = 0
@app.route('/sfeeder/feed', methods = ['GET','POST'])
def feed_permission():
    feedlog = dbm().feedlog
    feeders = dbm().feeders
    pets = dmb().pets
    resp = resp501
    if request.method == 'GET':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            entry = feeder.find_one({"key":data["key"]})
            if entry is not None:
                print(data, file=sys.stderr)
                print("feeder entry: ", entry, file = sys.stderr)
                    # If valid feed intial feedlog time is stored
                    if can_pet_feed(data["tag_uid"],entry["id"]):
                        feed = pets["tag_uid"]["food_quantity"]
                        resp = Response(dumps({"feed":feed}), status=200, mimetype='application/json')
            else :
                resp = Response(dumps({"feed":NO_FEED}), status=200, mimetype='application/json')

            resp = Response(dumps({"feed":KEY_INVALID}), status=200, mimetype='application/json')
    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            entry = feeder.find_one({"key":data["key"]})
            if entry is not None:
                # store base weight of bowl
                feedlog.update_one({"name":pet_name,"base_wt":NULL_WAIT}, {"$set":{"base_wt":data["base_wt"]}})
                resp = resp200

    return resp

#be able to get data on all pets in order to initalize local data or update local data
@app.route('/pets/', methods = ['GET'])
def get_all_pets():
    db = dbm().db
    pets = dbm().pets
    data = []
    if request.method == 'GET':
        #return all pets
        pet_cursor = pets.find({})
        if pet_cursor.count() > 0:
            for document in pet_cursor:
                data.append(document)
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

@app.route('/rfid_config/<pet_name>', methods = ['GET'])
def rfid_tag_config(pet_name):
    db = dbm().db
    pets = dbm().pets

    #here we'll be doing the math to get a tag id and put the id
    #into the rfid command queue for to be set to a tag

    if pets.find({"name":pet_name}).count() > 0:
        name = pet_name
        weight = pets.find_one({"name":pet_name})['weight']

        if len(name) > 16:
            name = name[:16]
        uid = 0
        #create number from chars of name
        for c in name:
            uid = (uid << 8) + ord(c)
        uid = uid + weight

        #get number of bytes from number
        #so we can fill the rest in with 0xFF
        length = 0
        temp_uid = uid
        while temp_uid != 0:
            temp_uid = temp_uid >> 8
            length += 1

        #fillin in
        for i in range(length,16):
            uid = (uid << 8) + 0xFF

        #put the bytes into array to be put into command queue
        listed = []
        temp_uid = uid
        for i in range(16):
            byt = temp_uid & 0xFF
            temp_uid = temp_uid >> 8
            listed.insert(0, byt)

        #next tag detected will have the calculated tag id written
        this_server.rfid_command_queue.put(listed)
        #put the uid into the db entry
        pets.update_one({"name":pet_name}, {"$set":{"tag_id":str(hex(uid))}})

        resp = resp200

    #this pet hasnt been created yet
    else:
        resp = resp501

    return resp

def run_server(queue):
    this_server.rfid_command_queue = queue
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=False)#runs on all local interfaces
    run_server(Queue())
