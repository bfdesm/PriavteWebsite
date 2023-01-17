import os

class RouteHandler(object):
    def __init__(self, base="index") -> None:
        self.base = base


    def searchFile(self, path):
        result = "404 Not Found"
        if path == "/":
            return result
        name = path.split("/")[-1]
        path = self.base + path.split("/" + name)[0]
        if "." not in name:
            name += ".html"
        for root, dirs, files in os.walk(path):
            if name in files:
                with open(path + "/" + name, encoding='utf-8') as file_obj:
                    contents = file_obj.read()
                    result = contents.rstrip()
                break
        return result

