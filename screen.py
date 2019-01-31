#!/usr/bin/python3

import sys
import asyncio
from pyppeteer import launch
#see /home/niles/.local/share/ for location of local chromium


async def screenshot(url,name,outdir):
    browser=await launch({'headless':True,'args':['--no-sandbox', '--disable-setuid-sandbox']})
    page =await browser.newPage()
    await page.goto(url,{'waitUntil':'networkidle0'})
    await page.screenshot({'path':outdir+name,'fullPage':True})
    await browser.close()
    #ofile=open("data.txt","a")
    #ofile.write(url+","+outdir+name+"\n")
    #ofile.close()

async def getScreenShot(url,name,outdir="./"):
    asyncio.get_event_loop().run_until_complete(screenshot(url,name,outdir))
    #asyncio.wait([screenshot(url,name,outdir)])
    #loop.run_until_complete(screenshot(url,name,outdir))    


if __name__=="__main__":
    if len(sys.argv) < 2:
        raise SystemError("screen: requires at least two args, screen <url> <name> <outdir=.>")

    outdir="./"
    url = sys.argv[1]
    if len(sys.argv) > 2:
        name = sys.argv[2]
    if len(sys.argv) > 3:
        outdir=sys.argv[3]
        if sys.path.isdir(outdir) == False:
            raise SystemError("screen: invalid outdir; "+outdir)

    getScreenShot(url,name,outdir)

