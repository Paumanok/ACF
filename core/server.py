#author: matthew smith mrs9107@g.rit.edu
#file: multithreaded http socket server

from http.server import BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import parse_qs
import io
import socket
import threading
import sys
import os
from multiprocessing import Process
import pdb

class server:
    default_version = "HTTP/0.9"
    content_type_text = "text/html"
    content_type_json = "application/json"
    enable_threading = "thread" #process, thread, None(process is bork)
    running_path = os.path.dirname(os.path.abspath(__file__))

    #initialize server socket
    def __init__(self, host, port, dbm):
        self.dbm = dbm
        self.host = host
        self.port = port
        #create tcp/ip socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.handlers = { "GET": lambda x: self.HTTP_GET(x)
                          }

        self.codes = {    "404": lambda x:self.HTTP_404(x),
                          "403": lambda x:self.HTTP_403(x),
                          "501": lambda x:self.HTTP_501(x)
                          }

    def listen(self):
        self.sock.listen(5) #backlog num, # of connections allowed to be queued
        processes = []

        while True:
            client, address = self.sock.accept()
            client.settimeout(60) #1 minute timeout
            if(self.enable_threading == "thread"):
                threading.Thread(target = self.handle_client, args= (client, address)).start()

            elif(self.enable_threading == "process"):
                process = Process(target = self.handle_client, args=(client, address))
                process.daemon = True
                process.start()

            else:
                self.handle_client(client, address)

    def handle_client(self, client, address):
        size = 1024
        while True:
            try:
            #if True:
                data = client.recv(size)
                print("gotsomething")
                if data:
                    #print(data)
                    response = self.handle_HTTP(data)
                    client.send(response)
                    client.close()
                else:
                    raise error('client disconnected')
                    print('cient disconnected')

            except:
            #else:
                client.close()

                return False

        return True


    def handle_HTTP(self, data):
        request = HTTP_request(data)
        command = request.command
        if not command in self.handlers.keys():
            return self.codes["501"](request)
        else:
            return self.handlers[command](request)

    #lil fatboi http_get method, with api documentation inline for now
    #qs = "json=<true/false>&pet_req=<true/false>&name=<pet_name>&date=<date/"">"
    #json - is this request for json data from db?
    #pet_req - is it asking for pet data or feed history
    #name - pet name
    #date - date of feed data if pet_req == false, otherwise, just empty string
    def HTTP_GET(self, request):
        #pdb.set_trace()
        args = parse_qs(request.path[2:]) #get args from request
        if(request.path == '/'):          #check if requesting default page
            file_size = os.path.getsize("hello.htm")
            file_name = "hello.htm"
            ct = self.content_type_text

        elif(args['json'][0] == 'true'):  #check if requesting json from db
            #pdb.set_trace()
            print("reached json block")
            f = self.HTTP_GET_JSON(request, args)
            print("past get json")
            file_size = len(f)
            ct = self.content_type_json

        else:                             #just go grab file being requested
            path = self.running_path + request.path
            if(os.access(path, os.R_OK)):
                if(os.path.exists(path)):
                    file_size = os.path.getsize(path)
                    file_name = request.path[1:]
                    f = (open(file_name).read())
                    ct = self.content_type_text
                else:
                    print(":it doesnt exist")
                    return self.codes["404"](request)
            else:
                print(":not allowed")
                return self.codes["403"](request)

        #construct response with content_type(ct),
        #file size, and string f as the file to be sent
        response = self.construct_header("200 OK",ct, file_size )
        response = (response + "\r\n" + f)
        print("constructed and sending response")

        return bytes(response, "utf8")

    #grab json data from db
    #todo:
    #need error checking for non existent animals
    #implement feed history grabbin
    def HTTP_GET_JSON(self, request, args):
        #use self.dbm
        print("reached http get json")
        print(args)
        if(args["pet_req"][0] == "true"):
            pet_name = args["name"][0]
            pet_data = self.dbm.get_by_name(self.dbm.pets, pet_name)
            file_size = len(pet_data)
            #response = self.construct_header("200 OK", \
            #       self.content_type_json, file_size)
            #response = response + "\r\n" + str(pet_data)
        #else:
            #do something for the feed history
        return str(pet_data)

#
#
#    def HTTP_PUT_JSON(self, request):
#        #use self.dbm
#
    def construct_header(self,response_status, content_type, content_length):
        time = 0
        #time = datetime.now().strftime('%b %d  %I:%M:%S\r\n')
        http_response = ("HTTP/1.1" + response_status + "\r\n" + \
                         "Server: python-custom\r\n" +\
                         "Content-Length: " + str(content_length) + "\r\n" + \
                         "Content-Type: " + content_type + "\r\n" + \
                         "Connection: Closed\r\n" )

        return http_response

#====================================================================
    def HTTP_501(self, request):
        construct_header("501 not implemented", content_type_text, 0)
        return 0

    def HTTP_404(self, request):
        file_size = os.path.getsize("htm/404.htm")
        response = self.construct_header("404",self.content_type_text, file_size )
        response = response + "\r\n" + (open("htm/404.htm").read())
        return bytes(response, "utf8")

    def HTTP_403(self, request):
        file_size = os.path.getsize("htm/403.htm")
        response = self.construct_header("403",self.content_type_text, file_size )
        response = response + "\r\n" + (open("htm/403.htm").read())
        return bytes(response, "utf8")
#====================================================================

#executive decision: project not about text parsing, so offload parsing
#to subset of HTTP library
#https://stackoverflow.com/questions/4685217/parse-raw-http-headers
class HTTP_request(BaseHTTPRequestHandler):

    def __init__(self, request):
        self.rfile = io.BytesIO(request)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


def main():
    port = 8080 #default http port
    server('', port).listen()


if __name__ == "__main__":
    main()
