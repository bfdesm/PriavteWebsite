
def generateHeader(protocolVersion="HTTP/1.1", statusCode="200", statusWord="OK", contentType="text/html;charset=utf-8", connection="keep-alive"):
    header = protocolVersion + " " + statusCode + " " + statusWord + '\n'
    header += "Content-Type: " + contentType + "\r\n"
    header += 'Connection: ' + connection + '\r\n'
    header += '\n'
    return header

def generateEndHeader():
    return generateHeader(connection="close")
