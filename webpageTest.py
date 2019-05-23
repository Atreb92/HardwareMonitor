import webview
import threading
import time
import sys
import random
import socket
import json


file = open('sample_hardwareInfo_dump.json', 'r', encoding='utf8').read()
hardwareInfo = json.loads(file)
update = True
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#hardwareInfo = {}

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.200', 10005)

html = open('page.html').read()

class blackboardFetcherThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        
    def run(self):
        global hardwareInfo
        try:
            while webview.window_exists(uid='master'):
                # Send data
                message = b'GET'
                #print('sending {!r}'.format(message))
                sock.sendall(message)
                
                hardwareInfo = json.loads(str(format(sock.recv(4096)))[2:-1])
                #print(hardwareInfo['nvidiagpu0']['temperature']['GPU Core'])
                #print(hardwareInfo)
                #updateHW(hardwareInfo)
                time.sleep(1)
        finally:
            print('closing socket')
            sock.close()
    

    

class Api:
    
    def getGPUTemp(self, params):
        response = {
            'id': 'response-container',
            'message': str(hardwareInfo['nvidiagpu0']['temperature']['GPU Core'])
        }
        return response



def create_app():
    webview.load_html(html)
    


t = threading.Thread(target=create_app)
t.start()
t2 = blackboardFetcherThread()
t2.start()
api = Api()
webview.create_window('HardwareMonitor', js_api=api, width=600, height=1024, resizable=False, debug=True)

    

