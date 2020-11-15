import subprocess
import socket
import signal
import time
import os

l = subprocess.Popen(['npm run dev'], shell=True, stdout=subprocess.DEVNULL ,cwd='/app/metacad', preexec_fn=os.setsid)
#test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#i = 1
#test_location = ('0.0.0.0', 3000)
#while bool(test_socket.connect_ex(test_location)) :
#       print("Waiting for socket at 3000 to open X" + str(i))
#       try:
#               i += 1
#               time.sleep(1)
#       except KeyboardInterrupt:
#               node.terminate()
#               sys.exit()

print("Connected")

input()
os.killpg(os.getpgid(l.pid), signal.SIGTERM)
