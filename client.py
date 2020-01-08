import socket

HOST = "192.168.1.34"
PORT = 8888

process_this_frame = True

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
# s.connect((HOST, PORT))

def send_message(message):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(message)
        data = s.recv(1024)
        process_this_frame != process_this_frame
        print(data)

# send_message(b'jkjhjh')