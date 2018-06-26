# Database Class
import MySQLdb

class DatabaseHandler:
    accound_id = 0
    username = ""
    password = ""
    
    def __init__(self):
        self.__handle = MySQLdb.connect("localhost","root","","socketdb")
        self.__cursor = self.__handle.cursor()
        self.__sql = ""
        
    def Verify_Credentials(self,username, password):
        self.username = username
        self.password = password
        self.__sql = "SELECT * FROM ACCOUNTS WHERE username='%s' AND password='%s'" % (self.username, self.password)
        self.__cursor.execute(self.__sql)
        count = self.__cursor.rowcount
        if count > 0:
            row = self.__cursor.fetchone()
            self.accound_id = row[0]
            return True
        else:
            return False
        
    def Get_Flags(self):
       self.__sql = "SELECT * FROM PERMISSIONS WHERE account_id=%d" % (self.accound_id)
       self.__cursor.execute(self.__sql)
       row = self.__cursor.fetchone()
       return row
    
    def Insert_File(self, filename, filetype, filesize):
        self.__sql = "INSERT INTO FILES VALUES('%s', '%s', %s)" % (filename, filetype, filesize)
        print ("Query: ", self.__sql)
        try:
            self.__cursor.execute(self.__sql)
            self.__handle.commit()
        except:
            self.__handle.rollback()
            
    def Get_Data(self):
        self.__sql = "SELECT * FROM FILES"
        self.__cursor.execute(self.__sql)
        results  = self.__cursor.fetchall()
        return results
        
    def Close_Connection(self):
        self.__handle.close()