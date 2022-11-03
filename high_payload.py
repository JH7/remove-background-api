import requests
import time
import threading

def send_request():
  request = requests.post("http://localhost:7888/", files = {
    'file': open('C:\\Users\\eintr\\Downloads\\3780760.jpg', 'rb')
  })

  if request.status_code != requests.codes.ok:
    print("Error: " + request.status_code) 


def start():
  threads = []
  num_of_threads = 200
  for i in range(num_of_threads):
    x = threading.Thread(target=send_request)
    x.start()
    threads.append(x)

  [x.join() for x in threads]

start()