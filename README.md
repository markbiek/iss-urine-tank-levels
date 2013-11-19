Simple python script which attempts to read the Urine Tank level of the ISS and post it to Twitter.

Since the ISS website loads its data asynchronously, we use the Selenium Webdriver (https://code.google.com/p/selenium/) module to launch
and invisible Firefox instance to load into the page.

This requires a headless X-server. We're using Xvfb (http://en.wikipedia.org/wiki/Xvfb).

How to launch Xvfb:

    Xvfb :1 &

    export DISPLAY=:1

This Stackoverflow question (http://stackoverflow.com/a/4474362/305) has a great example of how to
generate Twitter access tokens and interact with Twitter.

Latest Twitter api module (which uses v1.1) is on github https://github.com/bear/python-twitter
