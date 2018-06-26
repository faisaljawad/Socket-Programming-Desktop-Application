# Server Main
import socket
import _thread
import SocketHandler

def Client_Thread(ClientSocket, Address):
    myObj = SocketHandler.SocketHandler(ClientSocket, Address)
    myObj.EngageClient()

subnet_ipv4 =  socket.gethostbyname(socket.gethostname())
listening_port = 1234
print ("IP Address: ",subnet_ipv4)
print ("Port: ",listening_port)
ServerSocket = socket.socket()
ServerSocket.bind((subnet_ipv4,listening_port))
ServerSocket.listen(10)

while True:
    _thread.start_new_thread(Client_Thread, (ServerSocket.accept()))