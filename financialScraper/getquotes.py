# import urllib
# import json

# symbolslist = open("BloombergSymbols.txt").read()
# symbolslist = symbolslist.split(",")
# for symbol in symbolslist:
# 	htmltext = urllib.urlopen("http://bloomberg.com/markets/chart/data/1D/"+symbol)
# 	# newhtmltext = htmltext.read()
# 	# print newhtmltext
# 	try:
# 		data = json.load(htmltext)
# 		datapoints = data["data_values"]
# 		# for point in datapoints:
# 		# 	print "symbol",symbol, "time", point[0], "price", point[1]
# 		# 	print "the number of points is ", len(datapoints)
# 		try:
# 			print datapoints
# 			#print datapoints[len(datapoints)-1][1]
# 		except:
# 			print datapoints
# 	except ValueError:
# 		print symbol

import ystockquote
from pprint import pprint

symbolfile = open('Symbols.txt', 'r')
symbolstring = symbolfile.read()
symbollist = symbolstring.split(',')
for ticker in symbollist:
    pprint(ystockquote.get_all(ticker))
