# Socket Handler For Clients

import Database
import os
class SocketHandler:
    def __init__(self, ServerSocket, Address):
        self.ServerSocket = ServerSocket
        self.Address = Address
        self.dbHandle = Database.DatabaseHandler()
        self.message = ""
        self.answer = ""
        self.canUpload = False
        self.canDownload = False
    def EngageClient(self):
        if self.AskCredentials() == True:
            self.AskFlags()
            self.message = "option"
            self.ServerSocket.send(self.message.encode(encoding='ascii'))
            while True:
                self.answer = self.ServerSocket.recv(1024)
                self.answer = self.answer.decode(encoding='ascii')
                if self.answer == "list":
                    self.results = self.dbHandle.Get_Data()
                    self.message = str(len(self.results))
                    self.ServerSocket.send(self.message.encode(encoding='ascii'))
                    for row in self.results:
                        self.message = row[0]
                        #self.message = str(self.message)
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                        self.ServerSocket.recv(32)
                        self.message = row[1]
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                        self.ServerSocket.recv(32)
                        self.message = row[2]
                        self.message = str(self.message)
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                        self.ServerSocket.recv(32)
                elif self.answer == "upload":
                    if self.canUpload == True:
                        self.message = "start"
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                        self.answer = self.ServerSocket.recv(1024)
                        self.ServerSocket.send(("Ack").encode(encoding='ascii'))
                        filename = self.answer.decode(encoding='ascii')
                        self.answer = self.ServerSocket.recv(1024)
                        self.ServerSocket.send(("Ack").encode(encoding='ascii'))
                        filetype = self.answer.decode(encoding='ascii')
                        self.answer = self.ServerSocket.recv(1024)
                        self.ServerSocket.send(("Ack").encode(encoding='ascii'))
                        filesize = self.answer.decode(encoding='ascii')
                        filesize = int(filesize)
                        print ("File Size %d", (filesize))
                        file = open(filename,'wb')
                        filedata = self.ServerSocket.recv(filesize)
                        file.write(filedata)
                        file.close()
                        self.dbHandle.Insert_File(filename, filetype, filesize)
                    else:
                        self.message = "denied"
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                elif self.answer == "download":
                    if self.canDownload == True:
                        self.message = "start"
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                        self.answer = self.ServerSocket.recv(1024)
                        filename = self.answer.decode(encoding='ascii')
                        file_size = os.path.getsize(filename)
                        self.ServerSocket.send((str(file_size)).encode(encoding='ascii'))
                        self.ServerSocket.recv(32)
                        file = open(filename,'rb')
                        filedata = file.read(file_size)
                        self.ServerSocket.send(filedata)
                        file.close()
                    else:
                        self.message = "denied"
                        self.ServerSocket.send(self.message.encode(encoding='ascii'))
                elif self.asnwer == "exit":
                    break
        else:
            self.message = "invalid"
            self.ServerSocket.send(self.message.encode(encoding='ascii'))
            
    def AskCredentials(self):
        self.message="username"
        self.ServerSocket.send(self.message.encode(encoding='ascii'))
        self.username = self.ServerSocket.recv(1024)
        self.username = self.username.decode(encoding='ascii')
        self.message="password"
        self.ServerSocket.send(self.message.encode(encoding='ascii'))
        self.password = self.ServerSocket.recv(1024)
        self.password = self.password.decode(encoding='ascii')
        if self.dbHandle.Verify_Credentials(self.username, self.password) == True:
            return True
        else:
            return False
    
    def AskFlags(self):
        row = self.dbHandle.Get_Flags()
        self.canUpload = row[1]
        self.canDownload = row[2]