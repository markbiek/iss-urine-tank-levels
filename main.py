#!/usr/bin/python

from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import os
import re
import time
import sys
import twitter

def loadAccessToken():
    vals = {}
    tokenFile = 'access.token'

    if len(sys.argv) > 1:
        tokenFile = sys.argv[1]

    for line in open(tokenFile):
        (key, val) = line.strip().split('=')
        vals[key] = val

    return vals

#Check to see if we have a connection to the ISS
def checkIssStatus():
    """Looks like we get data on the page even if there's a No Signal message.
    Temporarily disabling this function until we figure it out"""
    return True
    """
    url = "http://spacestationlive.nasa.gov/status.indicator.html"

    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(5)

    soup = BeautifulSoup(browser.page_source)

    divStatus = soup.find(attrs={'class': 'los-state'})

    return "No signal" not in divStatus
    """

if __name__ == "__main__":
    tokens = loadAccessToken()
    if ("key" not in tokens.keys() or 
            "secret" not in tokens.keys() or 
            "consumer_key" not in tokens.keys() or 
            "consumer_secret" not in tokens.keys()):
        print "ERROR: Invalid access token file."
        sys.exit(1)

    os.environ['DISPLAY'] = ':1'

    api = twitter.Api(consumer_key=tokens['consumer_key'],
                        consumer_secret=tokens['consumer_secret'],
                        access_token_key=tokens['key'],
                        access_token_secret=tokens['secret'])
    status = ""

    if checkIssStatus():
        url = "http://spacestationlive.nasa.gov/displays/ethosDisplay3.html"

        browser = webdriver.Firefox()
        browser.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(browser.page_source)
        spanUPA = soup.find("span", {"id": "NODE3000005"})
        upaPer = spanUPA.text.strip()
        if re.search(r'^\d+\.*\d*%$', upaPer):
            status = time.strftime("%Y-%m-%d %H:%M:%S") + " - The ISS Urine Tank is currently " + spanUPA.text + " full."
    else:
        print "No connection to the ISS"
        sys.exit(3)

    if status !="":
        ret = api.PostUpdate(status)
        if ret is None:
            print "WARNING: PostUpdate returned None. Your post may have failed."
            sys.exit(2)
    else:
        print "ERROR: Invalid empty status."
        sys.exit(1)

    sys.exit(0)
