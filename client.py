import socket

# HOST = "192.168.1.33"
# PORT = 8888

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
# s.connect((HOST, PORT))

def send_message(message,host,port):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:

        try:
            s.connect((host, port))
            s.send(message)
        except ConnectionRefusedError:
            pass
        # data = s.recv(1024)
        # print(data)

# send_message(b'jkjhjh')