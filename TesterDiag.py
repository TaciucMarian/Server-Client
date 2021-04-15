import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50110        # The port used by the server

reply = ''
StateTracker = 0


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	while True:
		Input = input("Command: ")
		if Input == 'exit':
			break

		s.sendall(Input.encode())
		data = s.recv(1024)
		

		print('Received', repr(data))