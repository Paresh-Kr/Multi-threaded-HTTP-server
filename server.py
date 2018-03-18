'''
Created on Sep 6, 2017

@author: Paresh
'''


import socket
import os
import threading
import platform 
import posixpath
import mimetypes
import time
import re

base_path='www'

#default value for port and host
host=socket.gethostname()
port=47590

#def Response(connection, address,data):
def parse_RFC7231(date_str):
        
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
                  'sep', 'oct', 'nov', 'dec']
        formats = {
            # RFC 7231, e.g. 'Mon, 09 Sep 2011 23:36:00 GMT'
            r'^(?:\w{3}, )?(\d{2}) (\w{3}) (\d{4})\D.*$':
                lambda m: '{}-{:02d}-{}'.format(
                                          m.group(3),
                                          months.index(m.group(2).lower())+1,
                                          m.group(1))
        }

        out_date = None
        for regex, xform in formats.items():
            m = re.search(regex, date_str)
            if m:
                out_date = xform(m)
                break
        if out_date is None:
            print "DateFormatError"
        else:
            return out_date
    

class Server(object):

    def __init__(self,host,port): 
        # thread.__init__(self)
        self.clength=0
        self.Lastmodified=''
        self.filelist=['']
        self.ctype='' 
        self.ip = '' 
        self.port = port 
        self.mysocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip=socket.gethostbyname(self.ip)
        print "host name & port no of HTTP Server ::--" +socket.gethostname()+":",self.port
        #self.mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mysocket.bind((self.ip,self.port))
        #print "host name & port no  ::" +self.mysocket.getsockname()[0],self.mysocket.getsockname()[1]
        
        
    def ResponseHeader(self,val):
        
        header_response= ''
        content_type='' #have to calculate Content type (MIME)
        content_len=0   #calulate Content length
        if(val==True):
            header_response= 'HTTP/1.1 200 OK\n'
            content_type=self.ctype
            content_len=self.clength
            Lastmodified=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(int(self.Lastmodified)))
        elif(val==False):
            header_response= 'HTTP/1.1 404 Not Found\n'
            content_type= 'text/plain; charset=utf-8' #resource not found
            Lastmodified=''
            
        #print "Local time "+ti
        Current_time=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        #print "Date :---"+Current_time
        #print "Modified :----"+str(time.localtime())
        #Current_date=parse_RFC7231(time.localtime())
        #parse_RFC7231(self.Lastmodified)
        header_response+='Date : ' + Current_time +'\n'
        header_response+='Server : ' +':'+'Multi-threaded HTTP server'+'\n'
        header_response+='Last-Modified :'+Lastmodified+'\n'
        header_response+='Content-Type :' +content_type+'\n'
        header_response+='Content-Length :' +str(content_len)+'\n'
        
        return header_response
        
    def getmimetype(self, path):

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types (/etc/mime.types)
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream' # Default
        })    
        
            
    def handler(self,connection,address):
        Server_msg=''
        start=time.clock()
        data=connection.recv(1024)
        #print "recieved data :--" +data
        #if data == "":
              #  break
        if data:
            decode_data = bytes.decode(data)
        Methode=decode_data.split(' ')[0]
        if (Methode =='GET'):
                file_split=decode_data.split(' ') #spliting to get file
                requested_file=file_split[1] #taking first element after splitting
                requested_file=requested_file.split('?')[0]  # removing argument
                self.filelist.append(str(requested_file))
                num=self.filelist.count(str(requested_file))
                Server_msg+= requested_file+'|'
                Server_msg+=str(address[0])+'|'   #for client ip
                Server_msg+=str(address[1])+'|'   #for client port
                filepath=base_path+requested_file
                self.ctype= self.getmimetype(filepath)
                if platform.system() == 'Windows':
                    self.Lastmodified= os.path.getctime(filepath)
                else:
                    current_path=os.getcwd()
                    tpath=current_path+"/"+filepath
                    #print "file path exist or not :-- " +tpath
                    if(os.path.exists(tpath)):
                        self.Lastmodified = os.stat(filepath)
                        self.Lastmodified=self.Lastmodified.st_mtime
                    else :
                        self.Lastmodified=''  
                try:
                    file_read=open(filepath,'rb')
                    file_content=file_read.read()
                    self.clength=len(file_content)
                    file_read.close()
                    response_header= self.ResponseHeader(True)
                except:
                    response_header= self.ResponseHeader(False)
                    file_content=" Error 404: Requested Resource doesn't exist"
                
                
                Server_Response='\n'+response_header.encode()
                Server_Response+='\n'
                Server_Response+=file_content
                #print "Send message Content :---"+Server_Response
                connection.send(Server_Response,len(Server_Response))
                end=time.clock()-start
                Server_msg+=str(num) +'\n'
                print ""+Server_msg
                connection.close()
                # print server side client ip,port,requested resorce andtime
                        
        #self.mysocket.close()       
    def start(self):
        self.mysocket.listen(5)
        while True:
            connection,address=self.mysocket.accept()
            t=threading.Thread(target=self.handler,args=(connection,address))
            #t.setDaemon(True)
            t.start()

        self.mysocket.close()
#sock, addr = mySocket.accept()
#print ("Connection from: " + str(addr))

if __name__ == '__main__':
    current_path=os.getcwd()
    test_path=current_path +"/www"
    #print "Test Path--"+test_path
    if(os.path.exists(test_path)):
        server=Server('0.0.0.0',port).start()
    else :
        print "Resource Directory not present"
        exit()

