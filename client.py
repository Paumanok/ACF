#author: matthew smith mrs9107@g.rit.edu
#file: multithreaded http socket client

import socket
import sys
import threading
import time

#0 indexed
thread_max = 100

get_end = "HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0\r\nAccept: \
            text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en- US,en;q=0.5\r\nAccept-Encoding: gzip,\
            deflate\r\nDNT: 1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n"

pet_get = "GET /?json=true&pet_req=true&name=sniffles "

class client:


    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 8080)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        return sock

    def send(self, get_param):
        sock = self.connect()
        recv_data = ""
        data = True

        message = bytes(get_param, 'utf8')
        print("sending message")
        sock.sendall(message)

        while data:
            data = sock.recv(1024)
            recv_data += str(data)
            print('recieved: ' + str(data))

        sock.close()
        return recv_data

    def spam(self):
        while True:
            self.send()
            time.sleep(.1)

def main():

    c = client()
    #threads = []
    c.send(pet_get + get_end)

main()
