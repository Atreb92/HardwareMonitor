#!/usr/bin/python3
import clr
import threading
import time
import socket
import sys
import json



server_address = ('192.168.1.200', 10005)
hardwareInfo = {}

class myServer (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      print ('starting up on %s port %s' % server_address)
      sock.bind(server_address)

      sock.listen(1)

      while True:
         # Wait for a connection
         print('waiting for a connection')
         connection, client_address = sock.accept()
         try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
               data = connection.recv(512)
               #print(format(data))
               if format(data) == "b\'GET\'":
                  #print("ok")
                  connection.sendall(json.dumps(blackboard).encode("utf-8"))
               if format(data) == "b\'\'":
                  print("client disconnected")
                  break     

         finally:
            # Clean up the connection
            connection.close()
      

class myThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      while 1:
         fetch_stats(HardwareHandle)
         #print(len(json.dumps(blackboard)))
         time.sleep(1)
         

def initialize_openhardwaremonitor():
   file = 'OpenHardwareMonitorLib'
   clr.AddReference(file)

   from OpenHardwareMonitor import Hardware

   handle = Hardware.Computer()
   handle.MainboardEnabled = False
   handle.CPUEnabled = False
   handle.RAMEnabled = True
   handle.GPUEnabled = False
   handle.HDDEnabled = True
   handle.Open()
   
   return handle


#Function that inserts into the dictionary all current detected hardware name
def update_Hardware_Info(handle):
   for i in handle.Hardware:
      info = str(i.Identifier).split('/')
      out = ''
      for j in info:
         out += j
      hardwareInfo[out] = str(i.Name)
      
def fetch_stats(handle):
   for i in handle.Hardware:
      info = str(i.Identifier).split('/')
      index = ''
      for j in info:
         index += j
      
      for sensor in i.Sensors:
         info = str(sensor.Identifier).split('/')
         out = ''
         for j in info:
            out += j
         #print(info)
         print(sensor.Name)
         print(sensor.Value)

   
HardwareHandle = initialize_openhardwaremonitor()
#update_Hardware_Info(HardwareHandle)
fetch_stats(HardwareHandle)
thread1 = myThread()
#thread2 = myServer()


# Start new Threads
thread1.start()
#thread2.start()

print ("Exiting Main Thread")