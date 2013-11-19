#!/usr/bin/python

from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import re
import time
import sys
import twitter

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def loadAccessToken():
    vals = {}

    for line in open('access.token'):
        (key, val) = line.strip().split('=')
        vals[key] = val

    return vals

#Check to see if we have a connection to the ISS
def checkIssStatus():
    url = "http://spacestationlive.nasa.gov/status.indicator.html"

    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(5)

    soup = BeautifulSoup(browser.page_source)

    divStatus = soup.find(attrs={'class': 'los-state'})

    return "No signal" not in divStatus

if __name__ == "__main__":
    tokens = loadAccessToken()
    if ("key" not in tokens.keys() or 
            "secret" not in tokens.keys() or 
            "consumer_key" not in tokens.keys() or 
            "consumer_secret" not in tokens.keys()):
        print "ERROR: Invalid access token file."
        sys.exit(1)

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
        print spanUPA
    else:
        status = "No connection to the ISS"

    if status !="":
        ret = api.PostUpdate(status)
        print ret
        sys.exit(0)
    else:
        print "ERROR: Invalid empty status."
        sys.exit(1)
