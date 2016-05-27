# coding=utf-8
import socket
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# ADDRESS = ('172.16.230.189', 8888)
ADDRESS = ('172.16.6.194', 8888)
connType = "done"

"""
开始连接，每一次连接都执行这个方法，使服务器获取连接名称
"""
def startConn(sock):
    hostname = socket.gethostname() #gethostname()返回运行程序所在的计算机的主机名-- Win7-PC
    print "-"*20,hostname,"-"*20
    msg = "connName: "+hostname+"Type: "+connType #connType = "done"
    sock.send(msg)   #send()用于向一个已经连接的socket发送数据，如果无错误，返回值为所发送数据的总数，否则返回SOCKET_ERROR
    res = sock.recv(1024)
    print res

"""
从服务器返回连接列表
"""
def getConnList(sock):
    print 'getList'
    time.sleep(2)
    sock.send('getList')
    res = sock.recv(1024)
    print str(res)

"""
指定agent执行操作
"""
def done(sock, connName, casetype, id ,name ):
    print u"指定执行"
    sock.send('done ' + ' ' + connName + ' ' + casetype + ' ' + id + ' ' + name)

"""
命令server指定client执行
"""
def getlist():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    startConn(sock)
    getConnList(sock)
    sock.close()

def runTest(conn, casetype, caseName, name):
    print "-"*20,conn
    print "-"*20,casetype
    print "-"*20,caseName
    print "-"*20,name
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建一个socket以连接服务器
    sock.connect(ADDRESS) # 使用socket的connect方法连接服务器
    startConn(sock)
    done(sock, conn, casetype, caseName , name)
    sock.close()  # 客户通过调用socket的close方法关闭连接

# getlist()
# runTest('172.16.6.6', '中文','1','1')
