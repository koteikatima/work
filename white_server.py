from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread

class ThreadedServer(Thread):
    def __init__(self, host, port, timeout=60, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        self.addres_to_send=None
        self.last_data=None
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('SERVER Starting...', '\n')

        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now())
            print('SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen(5)
        if self.debug:
            print(datetime.now())
            print('SERVER Listening...', '\n')
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout

            if self.debug:
                print(datetime.now())
                print('CLIENT Connected:', client, '\n')

            # start a thread to listen to the client
            Thread(target = self.listenToClient,args = (client,address)).start()

            # send the client a connection message
            # res = {
            #     'cmd': 'connected',
            # }
            # response = dumps(res)
            # client.send(response.encode('utf-8'))

    def listenToClient(self, client, address):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024
        while True:
            try:
                #data GUI
                if address==self.addres_to_send:
                    if self.last_data!=None:
                        client.send(self.last_data)
                        self.last_data = None

                    # data from NAP
                else:
                    data = client.recv(size)
                    if data:
                        if data == b"1":
                            self.addres_to_send=address
                            print("addres_to_send {}".format( self.addres_to_send))

                        #client.settimeout(self.timeout)

                        else:
                            self.last_data = data
                            print("data {}".format(data))
                            print("last_data {}".format( self.last_data))



                            #response = dumps(res)
                            #client.send(response.encode('utf-8'))
                    else:
                        raise error('Client disconnected')

            except:
                if self.debug:
                    print(datetime.now())
                    print('CLIENT Disconnected:', client, '\n')
                client.close()
                return False


if __name__ == "__main__":
    #ThreadedServer('127.0.0.1', 8008, timeout=20000, debug=True).start()
    ThreadedServer('10.128.0.28', 12001, timeout=20000, debug=True).start()