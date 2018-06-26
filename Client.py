# Client Code

import socket
import os
import sys

message = ""
answer = ""
if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int (sys.argv[2])
    #print("Here")
else:
    host = socket.gethostbyname(socket.gethostname())
    port = 1234    
mySocket = socket.socket()
mySocket.connect((host,port))
answer = mySocket.recv(1024)
answer = answer.decode(encoding='ascii')
if answer == "username":
    username = input("Enter Username: ")
    mySocket.send(username.encode(encoding='ascii'))
else:
    print("HERE")
    print("Problem With Server, Debugging Required")
    exit(1)

answer = mySocket.recv(1024)
answer = answer.decode(encoding='ascii')
if answer == "password":
    username = input("Enter Password: ")
    mySocket.send(username.encode(encoding='ascii'))
else:
    print("Problem With Server, Debugging Required")
    exit(1)

answer = mySocket.recv(1024)
answer = answer.decode(encoding='ascii')
if answer == "option":
    while True:
        print("Enter 'list' to get list of all files")
        print("Enter 'upload' to upload file")
        print("Enter 'download' to download file from server")
        option = input("Enter your choice: ")
        mySocket.send(option.encode(encoding='ascii'))
        if option == "list":
            msg = mySocket.recv(1024)
            msg = msg.decode(encoding='ascii')
            length = int(msg)
            for x in range(length):
                filename = mySocket.recv(1024)
                mySocket.send(("Ack").encode(encoding='ascii'))
                filename = filename.decode(encoding='ascii')
                filetype = mySocket.recv(1024)
                mySocket.send(("Ack").encode(encoding='ascii'))
                filetype = filetype.decode(encoding='ascii')
                filesize = mySocket.recv(1024)
                mySocket.send(("Ack").encode(encoding='ascii'))
                filesize = filesize.decode(encoding='ascii')
                print("-------------\nFileName: %s\nFileType: %s\nFileSize: %s\n-------------" %(filename,filetype,filesize))
        elif option == "upload":
            msg = mySocket.recv(1024)
            msg = msg.decode(encoding='ascii')
            if msg == "start":
               filename = input("Enter FileName in Current Folder: ")
               file = open(filename,'rb')
               file_extension = os.path.splitext(filename)[1]
               file_size = os.path.getsize(filename)
               mySocket.send(filename.encode(encoding='ascii'))
               mySocket.recv(32)
               mySocket.send(file_extension.encode(encoding='ascii'))
               mySocket.recv(32)
               mySocket.send((str(file_size)).encode(encoding='ascii'))
               mySocket.recv(32)
               print ("File Size %d", (file_size))
               filedata = file.read(file_size)
               mySocket.send(filedata)
               file.close()
            elif msg == "denied":
                print("You Don't Have Privelages For This Option")
        elif option == "download":     
            msg = mySocket.recv(1024)
            msg = msg.decode(encoding='ascii')
            if msg == "start":
               filename = input("Enter FileName To Download: ")
               mySocket.send(filename.encode(encoding='ascii'))
               filesize = mySocket.recv(1024)
               filesize = filesize.decode(encoding='ascii')
               mySocket.send(("Ack").encode(encoding='ascii'))
               filesize = int(filesize)
               file = open(filename, 'wb')
               filedata = mySocket.recv(filesize)
               file.write(filedata)
               file.close()
            elif msg == "denied":
                print("You Don't Have Privelages For This Option")
                
elif answer == "invalid":
    print("Invalid Credentials, Exiting Program.")
    mySocket.close()
    exit(1)
else:
    print("Problem With Server, Debugging Required")
    mySocket.close()
    exit(1)
mySocket.close()