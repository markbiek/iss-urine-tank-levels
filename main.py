#!/usr/bin/python

"""
Simple python script which attempts to read the Urine Tank level of the ISS and post it to Twitter.

Since the ISS website loads its data asynchronously, we use the Selenium Webdriver module to launch 
and invisible Firefox instance to load into the page.

This requires a headless X-server. We're using Xvfb (http://en.wikipedia.org/wiki/Xvfb).

How to launch Xvfb:
    Xvfb :1 &
    export DISPLAY=:1
"""

from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import re
import time
import sys

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
    if checkIssStatus():
        url = "http://spacestationlive.nasa.gov/displays/ethosDisplay3.html"

        browser = webdriver.Firefox()
        browser.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(browser.page_source)
        spanUPA = soup.find("span", {"id": "NODE3000005"})
        print spanUPA
    else:
        print "No connection to the ISS"
