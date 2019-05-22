#!/usr/bin/python3
import clr
import threading
import time
import socket
import sys
import json
import pprint



server_address = ('192.168.1.200', 10005)
hardwareInfo = {}
blackboard = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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


#Metodo che inserisce nel dizionario i vari componenti hardware in uso nel Computer
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

def update_blackBoard(sensor):
   if sensor.Name == 'CPU Core #1':
      if sensor.SensorType == 3:
         blackboard[2] = sensor.Value
      elif sensor.SensorType == 2:
         blackboard[4] = sensor.Value
      elif sensor.SensorType == 1:
         blackboard[3] = sensor.Value
   elif sensor.Name == 'CPU Core #2':
      if sensor.SensorType == 3:
         blackboard[5] = sensor.Value
      elif sensor.SensorType == 2:
         blackboard[7] = sensor.Value
      elif sensor.SensorType == 1:
         blackboard[6] = sensor.Value
   elif sensor.Name == 'CPU Core #3':
      if sensor.SensorType == 3:
         blackboard[8] = sensor.Value
      elif sensor.SensorType == 2:
         blackboard[9] = sensor.Value
      elif sensor.SensorType == 1:
         blackboard[10] = sensor.Value
   elif sensor.Name == 'CPU Core #4':
      if sensor.SensorType == 3:
         blackboard[11] = sensor.Value
      elif sensor.SensorType == 2:
         blackboard[12] = sensor.Value
      elif sensor.SensorType == 1:
         blackboard[13] = sensor.Value
   elif sensor.Name == 'CPU Total':
      blackboard[0] = sensor.Value
   elif sensor.Name == 'CPU Package':
      if sensor.SensorType == 2:
         blackboard[1] = sensor.Value
   elif sensor.Name == 'GPU Core':
      if sensor.SensorType == 2:
         blackboard[15] = sensor.Value
      elif sensor.SensorType == 1:
         blackboard[17] = sensor.Value
      elif sensor.SensorType == 3:
         blackboard[16] = sensor.Value
   elif sensor.Name == 'GPU Memory':
      if sensor.SensorType == 3:
         blackboard[18] = sensor.Value
   elif sensor.Name.startswith('Memory'):
      if sensor.SensorType == 3:
         blackboard[14] = sensor.Value

   else:
      if sensor.Hardware.Name.startswith('Samsung'):
         if sensor.SensorType == 2:
            blackboard[19] = sensor.Value
         elif sensor.SensorType == 3:
            blackboard[20] = sensor.Value
      elif sensor.Hardware.Name.startswith('WDC'):
         if sensor.SensorType == 2:
            blackboard[21] = sensor.Value
         elif sensor.SensorType == 3:
            blackboard[22] = sensor.Value



# Create new threads
   
HardwareHandle = initialize_openhardwaremonitor()
#update_Hardware_Info(HardwareHandle)
fetch_stats(HardwareHandle)
#thread1 = myThread()
#thread2 = myServer()


# Start new Threads
#thread1.start()
#thread2.start()

print ("Exiting Main Thread")