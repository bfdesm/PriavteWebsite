import time
import HttpFactory
import RouteHandler


class RequestHandler(object):
    def __init__(self, conn, addr, noteSystem=None, debug=False) -> None:
        self.conn = conn
        self.addr = addr
        self.noteSystem = noteSystem
        self.debug = debug
        self.routeHandler = RouteHandler.RouteHandler()


    def sendMsgToNote(self, grade, msg):
        if not self.debug:
            return
        msg = msg + " in " + self.getTime()
        if self.noteSystem == None:
            print("[" + grade + "]", msg)
        else:
            self.noteSystem.sendMsgToNote(grade, msg)


    def getTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


    def handlerRequest(self):
        self.sendMsgToNote("INFO", "waitConnect: server: " + str(self.addr) + " client connect to me successfully")
        status, data = self.getText()
        result = self.executeRequest(data)
        response = "404 Not Found"
        if result != None:
            response = self.routeHandler.searchFile(result["path"])
        if "/css/" in result["path"]:
            header = HttpFactory.generateHeader(contentType="text/css")
        else:
            header = HttpFactory.generateHeader()
        response = header + response
        self.send(response)
        self.closeConn()


    def getText(self):
        data = str(None)
        length = 0
        try:
            if self.conn is None:
                return False, data
            # data = self.recv_content(conn, 700)
            data = self.conn.recv(1024 * 1024)
            return True, data
        except Exception as e:
            self.sendMsgToNote("INFO", "getText: " + str(e))
            self.sendMsgToNote("WARN", "False  length : " + str(length) + " data : " + data)
            return False, data


    def executeRequest(self, data):
        if data == "None":
            return None
        if not isinstance(data, str):
            data = data.decode()
        datas = data.split("\r\n")
        result = {}
        first = datas[0].split(" ")
        result["method"] = first[0]
        result["path"] = first[1]
        result["httpversion"] = first[2]
        for i in range(1, len(datas)):
            index = 0
            tmpdata = datas[i]
            for index in range(len(tmpdata)):
                if tmpdata[index] == ":":
                    break
            key = tmpdata[:index]
            value = tmpdata[index + 1:].strip()
            result[key] = value
        if "" in result:
            result.pop("")
        result["addr"] = self.addr
        result["conn"] = self.conn
        print(result)
        return result


    def endTcp(self):
        data = HttpFactory.generateEndHeader()
        self.send(data)


    def send(self, data):
        byteData = str(data).encode()
        try:
            self.conn.send(byteData)
        except Exception as e:
            self.sendMsgToNote("INFO", "sendText: client: server`s reflect is timeout")


    def closeConn(self):
        if self.conn != None:
            self.conn.close()

