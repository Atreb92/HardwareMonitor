#!/usr/bin/python3
import clr
import threading
import time
import socket
import sys
import json



server_address = ('192.168.1.200', 10005)

hardwareInfo = {}

updateBlackboard = True

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

            while True:

               data = connection.recv(4096)
               #print(format(data))
               if format(data) == "b\'GET\'":
                  #print("ok")
                  connection.sendall(json.dumps(hardwareInfo).encode("utf-8"))
               if format(data) == "b\'\'":
                  print("client disconnected")
                  break
         except:
            print("Error connection lost")     

         finally:
            # Clean up the connection
            connection.close()
      
class blackboardUpdaterThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
      update_Hardware_Info(HardwareHandle)
   def run(self):
      while updateBlackboard:
         fetch_stats(HardwareHandle)
         time.sleep(1)
         #print(hardwareInfo)
      print('thread closing')        

def initialize_openhardwaremonitor():
   file = 'OpenHardwareMonitorLib'
   clr.AddReference(file)

   from OpenHardwareMonitor import Hardware

   handle = Hardware.Computer()
   handle.MainboardEnabled = False
   handle.CPUEnabled = True
   handle.RAMEnabled = True
   handle.GPUEnabled = True
   handle.HDDEnabled = True
   handle.Open()
   
   return handle

#Function that inserts into the dictionary all current detected hardware name
def update_Hardware_Info(handle):
   for i in handle.Hardware:
      #converts the hardware identifiera from:
      #example:
      #/mainboard/0
      #to:
      #mainboard0
      info = str(i.Identifier).split('/')
      out = ''
      for j in info:
         out += j
      
      #adds to the dictionary using the previously created id as key and the hardware name as value
      hardwareInfo[out] = {'name': str(i.Name)}
         
def fetch_stats(handle):
   for i in handle.Hardware:
      #gets the index for the current hardware
      info = str(i.Identifier).split('/')
      #gets current index length
      indexLen = len(info)
      index = ''
      for j in info:
         index += j
      #updates with recents values
      i.Update()
      for sensor in i.Sensors:
         info = str(sensor.Identifier).split('/')

         #info[indexLen] contains the current type of value
         #example:
         #/hdd/2/temperature/0
         #
         #['', 'hdd', '2', 'temperature', '0']
         #
         #info[indexLen] is 'temperature'

         #might not be the best usage of try/catch...
         #try: add the value to current dictionary key, if its the first time it does the won't exsist so an error will occur
         #except: creates a new entry for that key
         try:
            hardwareInfo[index][info[indexLen]][sensor.Name] = sensor.Value
         except:
            hardwareInfo[index][info[indexLen]] = {sensor.Name: sensor.Value}

   
HardwareHandle = initialize_openhardwaremonitor()
#update_Hardware_Info(HardwareHandle)
#fetch_stats(HardwareHandle)

#converts to json, around 1600 char of information
#print(json.dumps(hardwareInfo))

thread1 = blackboardUpdaterThread()
thread2 = myServer()


# Start new Threads
thread1.start()
thread2.start()

#debugging
#time.sleep(5)
#updateBlackboard=False


print ("Exiting Main Thread")