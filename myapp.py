#!/usr/bin/python3

#from flask import Flask, request, Response
from quart import Quart,request,Response
import sys
import os
import screen
import asyncio
from zipfile import ZipFile
from zipfile import ZipInfo



#app = Flask(__name__)
app = Quart(__name__)

ROOTDIR="/tmp/"
#ROOTDIR="./"
PUPPET_DIR="XDG_DATA_HOME"
SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
CHROME_DIR=os.path.join(SCRIPT_DIR,"chrome")
PUPPET_CHROME_DIR="pyppeteer/local-chromium/575458/chrome-linux"


class MyZipFile(ZipFile):

    def extractall(self, path=None, members=None, pwd=None):
        if members is None:
            members = self.namelist()

        if path is None:
            path = os.getcwd()
        else:
            path = os.fspath(path)

        for zipinfo in members:
            self.extract(zipinfo, path, pwd)
            
    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        os.chmod(ret_val, attr)
        return ret_val


def extractChrome():
    outpath=os.path.join(os.environ.get("XDG_DATA_HOME"),PUPPET_CHROME_DIR)
    if os.path.isdir(outpath) == False:
        os.makedirs(outpath)
    
    cfile=os.path.join(CHROME_DIR,"chrome.z")
    if os.path.isfile(cfile) != True:
        raise SystemError("extractChrome:: no such archive chrome zip file "+cfile)
    archive=MyZipFile(cfile)
    archive.extractall(path=outpath)

loop = asyncio.get_event_loop()
    
@app.route('/',methods=['GET','POST'])
def welcome():
    return 'Welcome to Screenshot'


@app.route('/screenshot',methods=['GET'])
#async def url3screenshot():
def url2screenshot():
    outpath=os.path.join(os.environ.get("XDG_DATA_HOME"),PUPPET_CHROME_DIR)
    if os.path.isfile(os.path.join(outpath,"chrome")) != True:
        extractChrome()
    
    url = request.args.get('url')
    print("url : "+url)
    asyncio.wait([screen.screenshot(url,"out.png",ROOTDIR)])    

    res=open(ROOTDIR+"out.png", "rb", buffering=0)
    res=res.read()

    return Response(response=res, status=200, mimetype='image/png')    
        

if __name__ == '__main__':
    app.run()


