#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")


message = {'eui': '0004A30B002852FD',
           'payload': '01FC0C02FFFF030000041F0005F0D8060300'}
while True:
    # socket.send_json(message)
    socket.send_string('hello')

    print(socket.recv_string())

    time.sleep(5)

#  Do 10 requests, waiting each time for a response
# for request in range(10):
#     print("Sending request %s …" % request)
#     socket.send(b"Hello")

#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))
