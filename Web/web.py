#------------------------------------------------------------#
# Program: web.py
# Purpuose: The Web Server
#
# Group Member:
#          Victor Ding 1000272
#          Zhuolin He 965346
#          Chenyao Wang 928359
#          Danyang Wang 963747
#          Yuming Zhang 973693
#------------------------------------------------------------#

# Import Packages
import argparse
import couchdb, couchdb.design
import jsmin
import json
import os
import tornado.httpclient
import tornado.ioloop
import tornado.web

# Create CouchDB views
def CreateView(database, mapper, reducer=None):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), mapper+".js")
    with open(filename) as file:
        view = couchdb.design.ViewDefinition("analysis", mapper, jsmin.jsmin(file.read()), reducer)
        view.get_doc(database)
        view.sync(database)

# Initialize database instances
def InitializeDataBase():
    for address in ["172.26.37.250", "172.26.37.201"]:
        server = couchdb.Server("http://admin:123456@%s:5984/" % address)
        database = server["processed"]
        CreateView(database, "sum", "_sum")
        CreateView(database, "count", "_count")


# URL to the load balancer of CouchDB database instances
DATABASE = "http://127.0.0.1:5984/"

class BaseHandler(tornado.web.RequestHandler):
    def keywords(self):
        return ["sentiment", "pride", "greed", "lust", "envy", "gluttony", "wrath", "sloth"]

# Web handler for /data.json
class DataHandler(BaseHandler):
    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        async def _fetch(view):
            response = {}
            federal = await http.fetch(DATABASE + "/processed/_design/analysis/_view/" + view + "?group_level=0")
            state   = await http.fetch(DATABASE + "/processed/_design/analysis/_view/" + view + "?group_level=1")
            response["Federal"] = json.loads(federal.body.decode())["rows"][0]["value"];
            for entry in json.loads(state.body.decode())["rows"]:
                response[entry["key"]] = entry["value"]
            return response
        count = await _fetch("count")
        data  = await _fetch("sum")
        
        for region in data:
            for keyword in data[region]:
                data[region][keyword] /= count[region]
        self.write(data)

# Web handler for /analysis/(.*)
class AnalysisHandler(BaseHandler):
    def get(self, current):
        self.render("template/analysis.html", current=current, keywords=self.keywords())

# Web handler for the main page
class MainHandler(BaseHandler):
    def get(self):
        self.render("template/main.html", current="overview", keywords=self.keywords())

# Program entry
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000)
    args = parser.parse_args()

    # The first instance of Web Server should initialize database instances
    if (args.port == 8000):
        InitializeDataBase()

    tornado.web.Application([
        (r"/", MainHandler),
        (r"/analysis/(.*)", AnalysisHandler),
        (r"/data.json", DataHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "static"))),
    ]).listen(args.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.current().start()
