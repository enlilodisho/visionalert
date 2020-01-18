import socket
from threading import Thread

class TCPServer:

    # TCP Server Constructor
    def __init__(self, port):
        print("TCPServer Constructor");
        self.port = port

        # Server Status
        self.running = False

        # Set up socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', port))
        
        # Keep track of all running threads
        self.threads = []

    # TCP Server Destructor
    def __del__(self):
        self.socket.sendall(bytes([0x0F]))
        self.socket.shutdown()

    # Starts the server
    def start(self):
        self.socket.listen(5)
        self.running = True
        print("TCP server started on port {0}. Listening for connections...".format(self.port))

        # Accept connections
        while self.running:
            # Accept incomming connection
            (conn, (ip,port)) = self.socket.accept()

            # Create new thread for connection
            newThread = TCPClientThread(conn, ip, port)
            newThread.start()
            self.threads.append(newThread)

            # Send sample object
            conn.send(bytes([0x01,0x01,0x03,0xFA,0x70, 0x65, 0x72, 0x73, 0x6F, 0x6E]))

        for thread in self.threads:
            thread.join()

    # Stops the server
    def stop(self):
        print("Stopping server...")
        self.socket.sendall(bytes([0x0F]))
        for thread in self.threads:
            thread.join()

    # Gets the number of clients connected to server
    def getNumberOfClients(self):
        return len(self.threads)


# Client thread for every connection.
class TCPClientThread(Thread):
    
    def __init__(self, conn, ip, port):
        Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        self.once = False
        print("[+] New thread created for {0}:{1}".format(ip, port))

    def run(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if len(data) == 0 or data[0] == 0x0F:
                    print("Client {0}:{1} disconnected.".format(ip, port))
                    self.conn.shutdown()
                    break
            except:
                print("[-] Thread stopped for {0}:{1}. Client Disconnected.".format(self.ip, self.port))
                break

            print("Server received data from {0}:{1}".format(self.ip, self.port))

