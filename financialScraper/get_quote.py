from getqf import load_files
from gevent.pool import Pool
from urllib2 import Request, urlopen
import pandas as pd
def _request(param):
    """

    """
    symbol = param[0]
    dictionary = param[1]
    price, change = ('l1', 'c')
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, price)
    req = Request(url)
    resp = urlopen(req, timeout = 5)
    currentprice = resp.read().decode().strip()

    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, change)
    req = Request(url)
    resp = urlopen(req, timeout = 5)
    currentchange = resp.read().decode().strip()
    numchange, perchange = currentchange.split(' - ')
    dictionary[symbol] = (currentprice, numchange, perchange)
    print dictionary[symbol]

def get_quote(symbollist, ext = ''):
    """
Takes a list of symbols and uses ystockquote to request current stock information. \
Returns a dictionary with the keys as symbols, and the values being a dictionary of current stock
information. 
    """
    stock_dict = {}
    for index, symbol in enumerate(symbollist):
        symbollist[index] = (symbol + ext, stock_dict)
    pool = Pool(5)
        ##map symbol list to _get_data() fn. return tuple, with (symbol, statlist).
    pool.map(_request, symbollist)
    return pd.DataFrame.from_dict(stock_dict, orient = 'index')

def current_quote():
    indexlist = []
    indexlist.append('dataFiles/nsdqctsymbols.csv')
    indexlist.append('dataFiles/nsdqesymbols.csv')
    indexlist.append('dataFiles/nyesymbols.csv')
    indexlist.append('dataFiles/tsxogsymbols.csv')
    indexlist.append('dataFiles/tsxctsymbols.csv')
    indexlist.append('dataFiles/tsxvctsymbols.csv')
    indexlist.append('dataFiles/tsxvogsymbols.csv')


    indexlist = load_files(indexlist)

    current_quotes = {}
    for index, symbollist in indexlist.iteritems():
        #print index
        if index == 'tsxvctsymbols.csv' or index == 'tsxvogsymbols.csv':
            current_quotes[index] = get_quote(symbollist, '.V')
        elif index == 'tsxctsymbols.csv' or index == 'tsxogsymbols.csv':        
            current_quotes[index] = get_quote(symbollist, '.TO')
        else:
            current_quotes[index] = get_quote(symbollist)
    return current_quotes
if __name__ == '__main__':
    cq = current_quote()
