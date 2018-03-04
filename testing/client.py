#author: matthew smith mrs9107@g.rit.edu
#file:  http socket client testing database requests

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

new_pet_post = "POST / HTTP/1.1\r\nHost: localhost:8080\r\nConent-Type: application/json\r\nContent-length: "
new_pet_post_end = "json=true&pet_req=false&name=snuggles "
new_pet_post_content = "fug"


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
        #    print('recieved: ' + str(data))

        #here i'm grabbing only the json response.
        #at the end of the header before json, you see "Closed\r\n\r\n"
        #i split on 'Closed' and advance by 8 and terminate 4 from the EOL
        #to just print the data. You will need to find this json in Kotlin & C
        parts = recv_data.split('Closed')
        print(parts[1][8:-4])

        sock.close()
        return recv_data


def main():

    c = client()
    c.send(pet_get + get_end)


