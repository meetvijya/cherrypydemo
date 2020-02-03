import csv, redis, json,os
# download from web

from io import BytesIO
from zipfile import ZipFile
import requests, re, urllib

def DownloadAndExtractZipFile():
    zip_loc = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx"

    # connect to a URL
    website = urllib.request.urlopen(zip_loc)

    # read html code
    html = website.read()

    # use re.findall to get all the links
    # b'"((http|ftp)s?://.*?)"'.decode(encoding)
    links = re.findall("http://www.bseindia.com/download/BhavCopy/Equity/.*_CSV.ZIP", html.decode('utf-8'))
    if(len(links) > 0):
        content = requests.get(links[0])

        # unzip the content
        f = ZipFile(BytesIO(content.content))
        f.extractall()  # f.extract("EQ080120.CSV")
        f.printdir()
        # print(f.namelist()[0])
        filepath = os.getcwd() + '\\' + f.namelist()[0]
        # filepath = os.path.join(os.getcwd(), f.namelist()[0])
        return filepath
    else:
        return ""

def file_is_empty(filepath):
    return os.stat(filepath).st_size == 0

def read_csv_data(csv_file, i,j,k,l,m,n):
    with open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf)
        next(csvf)
        return [(r[i], r[j], r[k], r[l], r[m], r[n]) for r in csv_data]
stockdata =[]
def store_data(conn, data):
    for i in data:
        stockdata.append({"Code":i[0],"Name": i[1],"Open":i[2],"High": i[3],"Low":i[4],"Close": i[5]})
    return stockdata

def main():
    REDIS_HOST = 'localhost'
    PORT = 6379
    filepath = DownloadAndExtractZipFile()
    # extracting field name
    if(filepath):
        data = read_csv_data(filepath, 0,1,4,5,6,7)
        conn = redis.Redis(REDIS_HOST,PORT)
        SC = json.dumps(store_data(conn, data))
        conn.set("company",SC)
        print(json.loads(conn.get('company').decode('utf-8')))
        file_name = os.path.basename(filepath )
        #Delete the downloaded csv file after storing in database
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print("The file does not exist")
        return (file_name +' file downloaded successfully !')
    else:
        return ('File not Found.')
if '__main__' == __name__:
    main()
