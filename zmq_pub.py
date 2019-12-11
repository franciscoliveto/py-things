import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

message = {'key1': 'value1', 'key2': 'value2'}

while True:
    #  Send a message to subscribers.
    print('Sending a serialized python object...')
    socket.send_json(message)
    #socket.send(b'some data')

    time.sleep(2)
