import time

class RequestHandler(object):
    def __init__(self, conn, addr, noteSystem=None, debug=False) -> None:
        self.conn = conn
        self.addr = addr
        self.noteSystem = noteSystem
        self.debug = debug
        self.initmsg = {"text": "hello, it is my ASP"}


    def sendMsgToNote(self, grade, msg):
        if not self.debug:
            return
        msg = msg + " in " + self.getTime()
        if self.noteSystem == None:
            print("[" + grade + "]", msg)
        else:
            self.noteSystem.sendMsgToNote(grade, msg)


    def handlerRequest(self):
        self.sendMsgToNote("INFO", "waitConnect: server: " + str(self.addr) + " client connect to me successfully")
        status, data = self.getText()
        result = self.executeRequest(data)
        reponse = self.initmsg
        self.sendText(reponse)
        # self.sendText(json.dumps(self.initmsg), conn)
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
        result = {"first": datas[0]}
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


    def sendText(self, data):
        try:
            header = 'HTTP/1.1 200 OK\n'
            header += 'Content-Type: text/html;charset=utf-8\r\n'
            header += 'Connection: keep-alive\r\n'  # 和客户端保持长连接
            header += '\n'
            print(header + data)
            byteData = str(data).encode()
            self.conn.send(header.encode() + byteData)
            # self.conn.send(byteData)
        except Exception as e:
            self.sendMsgToNote("INFO", "sendText: client: server`s reflect is timeout")


    def closeConn(self):
        if self.conn != None:
            self.conn.close()


    def getTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

