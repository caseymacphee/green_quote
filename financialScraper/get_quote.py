from getqf import load_files
from gevent.pool import Pool
from urllib2 import Request, urlopen
import pandas as pd
def _request(param):
    symbol_with_ext = param[0]
    dictionary = param[1]
    index = param[2]
    symbol = param[3]
    price, change = ('l1', 'c')
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol_with_ext, price)
    req = Request(url)
    resp = urlopen(req, timeout = 5)
    currentprice = resp.read().decode().strip()

    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol_with_ext, change)
    req = Request(url)
    resp = urlopen(req, timeout = 5)
    currentchange = resp.read().decode().strip()
    numchange, perchange = currentchange.split(' - ')
    ###Converting the symbol to include an extension which in this case is the market and index###
    symbol = symbol + ':' + index
    
    dictionary[symbol] = [currentprice, numchange, perchange]
    print symbol, dictionary[symbol]

def get_quote(index, symbollist, ext = ''):
    """
Takes a list of symbols and uses ystockquote to request current stock information. \
Returns a dictionary with the keys as symbols, and the values being a dictionary of current stock
information. 
    """
    stock_dict = {}
    for i, symbol in enumerate(symbollist):
        symbollist[i] = (symbol + ext, stock_dict, index, symbol)
    pool = Pool(5)
        ##map symbol list to _get_data() fn. return tuple, with (symbol, statlist).
    pool.map(_request, symbollist)
    return stock_dict

def current_quote():
    """

    """
    indexlist = []
    indexlist.append('dataFiles/nsdqct.csv')
    indexlist.append('dataFiles/nsdqe.csv')
    indexlist.append('dataFiles/nye.csv')
    indexlist.append('dataFiles/tsxog.csv')
    indexlist.append('dataFiles/tsxct.csv')
    indexlist.append('dataFiles/tsxvct.csv')
    indexlist.append('dataFiles/tsxvog.csv')

    indexlist = load_files(indexlist)
    ### This looks like I should be using enumerate. #### 
    type(indexlist)
    current_quotes = []
    for index, symbollist in indexlist.iteritems():
        ### Defining indexes that come from the Toronto Stock Exchange, ###
        ### and adding the appropriate extension to their lookup symbol. ###
        if index == 'tsxvct.csv' or index == 'tsxvog.csv':
            current_quotes.append(get_quote(index, symbollist, '.V'))
        elif index == 'tsxct.csv' or index == 'tsxog.csv':        
            current_quotes.append(get_quote(index, symbollist, '.TO'))
        else:
            current_quotes.append(get_quote(index, symbollist))

    ###Combining them all into a conglomerated dictionary for data persistence in a ###
    ###Pandas dataframe.###
    quotes = current_quotes[0]
    for index in range(1, len(current_quotes)):
        quotes.update(current_quotes[index])
    return pd.DataFrame.from_dict(quotes, orient = 'index')

if __name__ == '__main__':
    cq = current_quote()
