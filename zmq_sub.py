import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    # Wait for a message
    message = socket.recv_json()
    #message = socket.recv()
    print('Received message %s' % message)
