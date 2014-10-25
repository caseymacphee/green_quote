import json
from gevent import monkey
import urllib2
from gevent.pool import Pool

symbolslist = open("BloombergSymbols.txt").read()
symbolslist = symbolslist.split(",")

for i, symbol in enumerate(symbolslist):
	symbolslist[i] = (symbol, "http://bloomberg.com/markets/chart/data/1D/" + symbol)
newdict = {}
def download(url):
	try:
		htmltext = urllib2.urlopen(url[1])
		# newhtmltext = htmltext.read()
		data = json.load(htmltext)
		datapoints = data["data_values"]
		newdict[url[0]] = datapoints

		try:
			print url[0],datapoints
			#print url[0],datapoints[len(datapoints)-1][1]]
		except:
			print 'no data for : ' + url[0]
	except:
		pass

urls = symbolslist
pool = Pool(20)

pool.map(download, urls)

# import gevent.monkey
# gevent.monkey.patch_socket()

# import gevent
# import urllib2
# import simplejson as json

# def fetch(pid):
#     response = urllib2.urlopen('http://www.bloomberg.com/markets/chart/data/1D/XOM:US')
#     result = response.read()
#     json_result = json.loads(result)

#     print json_result['data_values']

# def synchronous():
#     for i in range(1,10):
#         fetch(i)

# def asynchronous():
#     threads = []
#     for i in range(1,10):
#         threads.append(gevent.spawn(fetch, i))
#     gevent.joinall(threads)

# print('Synchronous:')
# synchronous()

# print('Asynchronous:')
# asynchronous()

