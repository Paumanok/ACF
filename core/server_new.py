#author: matthew smith mrs9107
#file: server_new.py
#purpose: to move past that janky http server and move to flask

from flask import Flask
from database_manager import dbm
from config import *


app =  Flask("ACF")



@app.route('/pets/<pet_id>', methods = ['GET', 'POST', 'DELETE'])
def pet(pet_id):
    if request.method == 'GET':
       petname = request.form['pet_name'] #http something or other pets/

    elif request.method == 'POST':
        data = request.form

    elif request.method == 'DELETE':

    else:
        #error

if __name__ == "__main__":
    app.run(host+port)
