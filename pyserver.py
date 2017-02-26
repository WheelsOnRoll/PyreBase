import pyrebase
import socket
from subprocess import PIPE, Popen
import time, sys

HOST = ''
PORT = 8134
serverStatus = 0

config = {
	"apiKey"            : "AIzaSyABjB5OCyfUh3YbhMkcKsYZmqWgJcyJybM",
	"authDomain"        : "worapp-8bba7.firebaseapp.com",
	"databaseURL"       : "https://worapp-8bba7.firebaseio.com",
	"storageBucket"     : "worapp-8bba7.appspot.com",
	"messagingSenderId" : "786995450047",
	"serviceAccount"    : "WORAPP.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

#authenticate a user
user = auth.sign_in_with_email_and_password("pyserver@worapp-8bba7.iam.gserviceaccount.com", "d17aedfc4f85980f41ca34ab3c597b9e124e773c")

db = firebase.database()

# test = db.child("test").get()
# print(test)

def stream_handler(message):
	global p
	print(message["event"])
	print(message["path"])
	print(message["data"])
	if message["path"] == b'/':
		return;
	if serverStatus == 2:
		if message["data"] == True:
			p.stdin.write(b'1\n')
		else:
			p.stdin.write(b'0\n');
		p.stdin.flush()
		time.sleep(1);
		data = p.stdout.readline()
		print('Recieved: '+str(data));

my_stream = db.child("test").stream(stream_handler)

p = Popen(['./server'], stdin=PIPE, stdout=PIPE)

time.sleep(2)

out = p.stdout.readline()
print(out)
if b'Error' in out:
	sys.exit()

serverStatus = 1;
time.sleep(10);

out = p.stdout.readline()
print(out)
if b'Error' in out:
	sys.exit()

serverStatus = 2;
time.sleep(1);

# p.stdin.write(b'1\n')
# p.stdin.flush()
# data = p.stdout.readline()
# print(data)
