import socket
import random
import time
import threading
import RequestHandler


class ASP(object):
    def __init__(self, selfIP, selfPort, noteSystem=None, debug=False) -> None:
        self.selfIP = selfIP
        if selfPort != None:
            self.selfPort = int(selfPort)
        else:
            self.selfPort = selfPort
        self.connectdefaulttimeout = 5 + random.randint(0, 5)
        self.noteSystem = noteSystem
        self.debug = debug
        self.sendMsgToNote("INFO", "init: start server")
        while not self.buildServerSocket():
            pass
        self.connpool = {}
        thread = threading.Thread(target=self.waitConnect, args=())
        thread.setDaemon(True)
        thread.start()


    def sendMsgToNote(self, grade, msg):
        if not self.debug:
            return
        msg = msg + " in " + self.getTime()
        if self.noteSystem == None:
            print("[" + grade + "]", msg)
        else:
            self.noteSystem.sendMsgToNote(grade, msg)


    def buildServerSocket(self):
        try:
            self.serverSk = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM, proto=0)
            self.serverSk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSk.bind((self.selfIP, self.selfPort))
            self.serverSk.listen()
            self.sendMsgToNote("INFO", "buildServerSocket: server: listen to connect successfully")
            return True
        except Exception as e:
            if "[Errno 98] Address already in use" in str(e):
                print(e)
                time.sleep(1)
            self.sendMsgToNote("INFO", "buildServerSocket: " + str(e))
            return False


    def waitConnect(self):
        self.serverSk.settimeout(self.connectdefaulttimeout)
        beforetime = time.time()
        while True:
            try:
                conn, addr = self.serverSk.accept()
                if conn != None:
                    requestHandler = RequestHandler.RequestHandler(conn, addr, self.noteSystem, self.debug)
                    thread = threading.Thread(target=requestHandler.handlerRequest, args=())
                    thread.setDaemon(True)
                    thread.start()
            except Exception as e:
                nowtime = time.time()
                if "timed out" in str(e):
                    if nowtime - beforetime >= 30:
                        self.sendMsgToNote("INFO", "waitConnect: server: waiting for connect")
                        beforetime = nowtime
                else:
                    self.sendMsgToNote("INFO", "waitConnect: " + str(e))


    def closeAll(self):
        self.closeSocket()


    def closeSocket(self):
        self.serverSk.close()
        self.serverSk = None


    def getTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

