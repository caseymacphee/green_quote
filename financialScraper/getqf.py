#!/usr/bin/env python
import pandas as pd
import urllib2
import re
import datetime
from bs4 import BeautifulSoup
from gevent.pool import Pool

def load_files(symbolfilepaths, csvdelim = ","):
    """ 
Takes a list of symbol file paths to respective csv files, and loads their content into a \
dictionary of file-paths to lists containing the content of the csv. The delimeter of the csv files \
defaults to a ','. 
    """
    index_lists = {}
    for file in symbolfilepaths:
        symbol_file = open(file)
        symbol_string = symbol_file.read()
        symbol_list = symbol_string.split(",")
        symbol_file.close()
        path = file.split('/')
        name = path[len(path)-1]
        name = name.split('.')
        index_lists[name[0]] = symbol_list
    return index_lists

def get_data(symbollist, index_name, ext = ''):
    """
Takes a list of symbols, and requests the key statistics page from yahoo for that company. \
Searches for all the table data for that company and returns a dictionary of symbols for keys mapped to\
a list of statistical data for that information.
    """

    data_lists = {}
    for index, symbol in enumerate(symbollist):
        symbollist[index] = (symbol + ext, data_lists, index_name)
    pool = Pool(5)
        ##map symbol list to _get_data() fn. return tuple, with (symbol, statlist).
    
    pool.map(_get_data, symbollist)
    return data_lists

def _get_data(param):
    symbol = param[0]
    data_lists = param[1]
    index = param[2]
    url = "http://finance.yahoo.com/q/ks?s={}+Key+Statistics".format(symbol)
    try:
        resp = urllib2.urlopen(url, timeout = 10)

        if resp.getcode() == 200:
            htmltext = BeautifulSoup(resp.read())
            data_table_pattern = "yfnc_tabledata1"
            result_list = htmltext.findAll(class_= data_table_pattern)
            current_date_time = datetime.datetime.now()
            formatted_date_stamp = current_date_time.strftime("%A %B %d, %Y")
            
            result_list.insert(0,formatted_date_stamp)
            full_symbol = symbol + ':' + index
            table_data_list = []
            table_data_list.append(formatted_date_stamp)
            keystatrows = set([1,2,3,12,16,19,20,22,27,31,33,35,36,37,38,42,43,50,51,52,56,57])
            for index, stat in enumerate(result_list):
                if index in keystatrows:
                    stat_atom = stat.get_text()
                    if stat_atom is None or stat_atom == 'N/A':
                        stat_atom = 'NaN'
                    table_data_list.append(stat_atom)
            if len(table_data_list) < 2:
                print full_symbol, "Not found"
            else:
                print full_symbol, "Got data"
            
            data_lists[full_symbol] = table_data_list
        else:
            print resp.getcode(), symbol
    except:
        print "Timed out for {}".format(symbol)

    

def add_labels(data_lists, table_labels):
    """
Takes a dictionary with symbols for keys mapped to a list of statistic values.\
Returns a dictionary with symbols for keys mapped to a dictionary with the statistic label \
for keys, and the associated figure for the value. The new dictionary is returned
    """
    labeled_dictionary_collection = {}
    

    for symbol, data_list in data_lists.iteritems():
        if len(data_list) > 1:
            labeled_dictionary_collection[symbol] = dict(zip(table_labels,data_list))
    return labeled_dictionary_collection

def remove_number_symbols(data_lists):
    """
Takes a dictionary with symbols for keys mapped to a list of statistic values, and looks for placeholder values,\ 
replacing them with the appropriate number value. The function then returns a new dictionary with the changes made.
    """
    billion = 'B'
    million = 'M'
    thousand = 'K'
    percent = '%'
    dot = '\.'
    comma = ','
    B = re.compile(billion)
    M = re.compile(million)
    K = re.compile(thousand)
    Perc = re.compile(percent)
    Dot = re.compile(dot)
    Comm = re.compile(comma)

    fltpoint_dict = {}
    for symbol, datalist in data_lists.iteritems():
        new_data_list = []
        if len(datalist) > 1:
            for statistic in datalist:
                if percent in statistic:
                    statistic = Perc.sub('', statistic)
                    statistic = Comm.sub('', statistic)
                    new_data_list.append(float(statistic))
                elif comma in statistic or 'May' in statistic or 'Mar' in statistic:
                    statistic = Comm.sub('', statistic)
                    try:
                        statistic = float(statistic)
                    except:
                        pass
                    new_data_list.append(statistic)
                elif billion in statistic or million in statistic or thousand in statistic:
                    statistic = B.sub('0000000', statistic)
                    statistic = M.sub('00000', statistic)
                    statistic = K.sub('0', statistic)
                    statistic = Dot.sub('', statistic)
                    new_data_list.append(float(statistic))
                else:
                    try:
                        statistic = float(statistic)
                    except:
                        pass
                    new_data_list.append(statistic)
            fltpoint_dict[symbol] = new_data_list
        else:
            fltpoint_dict[symbol] = ['N/A']

    return fltpoint_dict

def run_stats(index_dicts):

    stat_dataframes = {}
    for index, company_dict in index_dicts.iteritems():
        index_df = pd.DataFrame.from_dict(company_dict, orient = 'index')
        print index_df
        stat_list = []
        for header, column in index_df.iteritems():
            try:
                stat_list.append(column.mean())
            except:
                stat_list.append('No mean available')
        stat_dataframes[index] = stat_list

    NA_stat_frame = pd.DataFrame.from_dict(stat_dataframes, orient = 'index')
    return NA_stat_frame

def combine_indexes(index_list):
    # print index_list[0]

    NA_companies = index_list[0]

    for index in xrange(1,len(index_list)):
        NA_companies.update(index_list[index])
    NA_companies_frame = pd.DataFrame.from_dict(NA_companies, orient = 'index')
    return NA_companies_frame

def scraper():
    indexlist = []
    indexlist.append('dataFiles/nsdqct.csv')
    indexlist.append('dataFiles/nsdqe.csv')
    indexlist.append('dataFiles/nye.csv')
    indexlist.append('dataFiles/tsxog.csv')
    indexlist.append('dataFiles/tsxct.csv')
    indexlist.append('dataFiles/tsxvct.csv')
    indexlist.append('dataFiles/tsxvog.csv')

    table_labels = [
    "Date Time Gathered",
    "Market Cap (intraday)5",
    "Enterprise Value 3",
    "Trailing P/E (ttm, intraday)",
    # "Forward P/E 1","PEG Ratio (5 yr expected) 1",
    # "Price/Sales (ttm)",
    # "Price/Book (mrq)",
    # "Enterprise Value/Revenue (ttm) 3",
    # "Enterprise Value/EBITDA (ttm) 6",
    # "Fiscal Year Ends",
    # "Most Recent Quarter (mrq)",
    "Profit Margin (ttm)",
    # "Operating Margin (ttm)",
    # "Return on Assets (ttm)",
    # "Return on Equity (ttm)",
    "Revenue (ttm)",
    # "Revenue Per Share (ttm)",
    # "Qtrly Revenue Growth (yoy)",
    "Gross Profit (ttm)",
    "EBITDA (ttm) 6",
    # "Net Income Avl to Common (ttm)",
    "Diluted EPS (ttm)",
    # "Qtrly Earnings Growth (yoy)",
    # "Total Cash (mrq)",
    # "Total Cash Per Share (mrq)",
    # "Total Debt (mrq)",
    "Total Debt/Equity (mrq)",
    # "Current Ratio (mrq)",
    # "Book Value Per Share (mrq)",
    # "Operating Cash Flow (ttm)",
    "Levered Free Cash Flow (ttm)",
    # "Beta",
    "52-Week Change3",
    # "S&P500 52-Week Change3",
    "52-Week High 3",
    "52-Week Low 3",
    "50-Day Moving Average 3",
    "200-Day Moving Average 3",
    # "Avg Vol (3 month) 3",
    # "Avg Vol (10 day) 3",
    # "Shares Outstanding 5",
    # "Float",
    "% Held by Insiders 1",
    "% Held by Institutions 1",
    # "Shares Short 3",
    # "Short Ratio 3",
    # "Short % of Float 3",
    # "Shares Short (prior month) 3",
    # "Forward Annual Dividend Rate 4",
    # "Forward Annual Dividend Yield 4",
    "Trailing Annual Dividend Yield 3",
    "Trailing Annual Dividend Yield3",
    "5 Year Average Dividend Yield 4",
    # "Payout Ratio 4",
    # "Dividend Date 3",
    # "Ex-Dividend Date 4",
    "Last Split Factor 2",
    "Last Split Date 3",]
    indexlist = load_files(indexlist)

    # # ##test grab##
    # testlist = ['dataFiles/nsdqct.csv']
    # testindexlist = load_files(testlist)
    # ##end here##

    ##Get the data and store it in a dict of indexes to company symbols to lists of values ##
    qfindexdict = {}
    for index, symbollist in indexlist.iteritems():
        print index
        if index == 'tsxvct' or index == 'tsxvog':
            qfindexdict[index] = get_data(symbollist, index, '.V')
        elif index == 'tsxct' or index == 'tsxog':
            qfindexdict[index] = get_data(symbollist, index, '.TO')
        else:
            qfindexdict[index] = get_data(symbollist, index)
    ## End data grab ##

    ##Take dict of indexes to company symbols to lists of values and return a dataframe of stats ##
    float_dict = {}
    for index, companydict in qfindexdict.iteritems():
        float_dict[index] = remove_number_symbols(companydict)
    ## End int conversion ##
    # Gather stats by index ##
    NA_energy_stat_frame = run_stats(float_dict)
    # Pool all companies ##
    
    qflist = []
    for index, companies in qfindexdict.iteritems():
        qflist.append(companies)

    NA_energy_frame = combine_indexes(qflist)

    # labeledindexdicts = {}
    # for index, companydict in qfindexdict.iteritems():
    #     labeledindexdicts[index] = add_labels(companydict, table_labels)

    # return fltpointmarketdicts, labeledindexdicts, current_quotes, day_quotes, month_quotes, year_quotes
    # return NA_energy_stat_frame, NA_energy_frame
    return NA_energy_frame, NA_energy_stat_frame
if __name__ == '__main__':
    NA_companies_frame, NA_energy_stats = scraper()
