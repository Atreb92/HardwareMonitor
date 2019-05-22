#socket_echo_client.py
import socket
import sys
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.200', 10005)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    while True:
        # Send data
        message = b'GET'
        print('sending {!r}'.format(message))
        sock.sendall(message)
        print("recieved: " + format(sock.recv(4096)))
        time.sleep(1)
    
    

finally:
    print('closing socket')
    sock.close()