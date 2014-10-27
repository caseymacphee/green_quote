#!/usr/bin/env python

import urllib2
import re
import json

def get_chart(symbol, timeframe = 'D', country = "US"):
    dash = '-'
    to_slash = re.compile(dash)
    symbol = to_slash.sub('/', symbol)
    print symbol
    url = "http://bloomberg.com/markets/chart/data/1{}/{}:{}".format(timeframe,symbol,country)
    resp = urllib2.urlopen(url)
    if resp.getcode() == 200:
        data = json.load(resp)
        datapoints = data["data_values"]
    else:
        print symbol, "\tN/A"
        datapoints = 'N/A'
    return datapoints