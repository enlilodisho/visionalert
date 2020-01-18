# Python TCP Client A
import atexit
import socket 

host = socket.gethostname() 
port = 5050
BUFFER_SIZE = 1024 

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect(('127.0.0.1', port))

fakemsg = bytes([0x02, 0x01, 0x09])
tcpClientA.send(fakemsg)

while True:
    data = tcpClientA.recv(BUFFER_SIZE).decode()

    if len(data) == 0 or data[0] == 0x0F:
        print("Server closed.")
        tcpClientA.shutdown(1)
        break

    print("Client2 received data:", data)
    tcpClientA.send(fakemsg)

tcpClientA.close() 

@atexit.register
def goodbye():
    tcpClientA.send(bytes([0x0F]))
    tcpClientA.shutdown()

