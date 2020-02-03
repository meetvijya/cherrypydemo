import cherrypy,redis,json,requests,os
from os.path import abspath
import cherryPyDemo.DownloadBSEEquityFile

REDIS_HOST = 'localhost'
PORT =  6379
conn = redis.Redis(REDIS_HOST,PORT)

CP_CONF = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./'), # staticdir needs an absolute path
             }
        }

class App:

    stockdata =[]
    @cherrypy.expose
    def index(self):
        return open("Views/index.html")

    @cherrypy.expose
    def SearchByComapanyDetails(self,name):

        stockdata = json.loads(conn.get('company'))

        result =[]
        for i in range(0, len(stockdata)):
            sd = (stockdata[i]['Name']).strip()
            if sd.startswith(name.upper()):
                #print(stockdata[i])
                result.append(stockdata[i])
        return json.dumps(result)

    @cherrypy.expose
    #@cherrypy.tools.json_out()
    def GetTopTenStockData(self):
        stockdata = json.loads(conn.get('company'))#.decode('utf-8'))
        if(len(stockdata) != 0):
            return json.dumps(stockdata[:10])
        else:
            return json.dumps('No Data Avialable.Click Download Button')

    @cherrypy.expose
    def DownloadCSV(self):
        res =cherryPyDemo.DownloadBSEEquityFile.main()
        return json.dumps(res)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8082})
    cherrypy.quickstart(App(), '/', CP_CONF)