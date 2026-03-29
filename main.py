import socket
from oscparser import OSCMessage, OSCEncoder, OSCDecoder, OSCFraming, OSCModes, OSCString, OSCInt, OSCFloat, OSCBlob, OSCTrue, OSCFalse, OSCMidi
import time
import os
import random

## Get the transport and framing from enviroment variables, with defaults

transport = os.getenv('transport', 'tcp').lower()
if transport not in ['tcp', 'udp']:
    raise ValueError(f"Invalid transport: {transport}. Must be 'tcp' or 'udp'.")
framing = os.getenv('framing', 'osc11').lower()
if framing not in ['osc11', 'osc10']:
    raise ValueError(f"Invalid framing: {framing}. Must be 'osc11' or 'osc10'.")

# If TCP transport is selected, prepare a socket to be ready to be connected to by clients.

if transport == 'tcp':
    mode = OSCModes.TCP
elif transport == 'udp':
    mode = OSCModes.UDP

if framing == 'osc11':
    framing_mode = OSCFraming.OSC11
elif framing == 'osc10':
    framing_mode = OSCFraming.OSC10
    

if transport == 'tcp':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9000))
    server_socket.listen(1)
    print("TCP server listening on port 9000")
    ## When a client connects, accept the connection and return 1 million osc messages as fast as possible.
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client connected from {addr}")
        encoder = OSCEncoder(mode=mode, framing=framing_mode)
        ## Start a timer to see how long it takes to send 1 million messages
        start_time = time.time()
        for i in range(1000000):
            print(i)
            ## choose a random ascii character
            
            msg = OSCMessage(address=f"/benchmark/{random.choice('abcdefghijklmnopqrstuvwxyz1234567890')}{random.choice('abcdefghijklmnopqrstuvwxyz1234567890')}{random.choice('abcdefghijklmnopqrstuvwxyz1234567890')}{random.choice('abcdefghijklmnopqrstuvwxyz1234567890')}{random.choice('abcdefghijklmnopqrstuvwxyz1234567890')}/wildcards", args=())
            encoded_msg = encoder.encode(msg)
            client_socket.sendall(encoded_msg)
        client_socket.close()
        end_time = time.time()
        print(f"Sent 1 million messages in {end_time - start_time} seconds")
        print(f"Average time per message: {(end_time - start_time) / 1000000 * 1000000} nanoseconds")