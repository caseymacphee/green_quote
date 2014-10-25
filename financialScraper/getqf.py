import urllib2
import re
import csv
import datetime
import pandas as pd
import ystockquote
from bs4 import BeautifulSoup
import json

##Get some data and saving it to disk

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

        #### This is an operation specific to your file system ####
        path = file.split('/')
        name = path[:-1].split(csvdelim)
        index_lists[name[0]] = symbol_list
    return index_lists


def get_data(symbollist):
    """
Takes a list of symbols, and requests the key statistics page from yahoo for that company. \
Searches for all the table data for that company and returns a list of that information.
    """
    data_lists = {}
    for symbol in symbollist:
        url = "http://finance.yahoo.com/q/ks?s={}+Key+Statistics".format(symbol)
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            htmltext = BeautifulSoup(resp.read())
            data_table_pattern = "yfnc_tabledata1"
            table_data_list = re.findall(data_table_pattern, htmltext)
            current_date_time = datetime.datetime.now()
            formatted_date_stamp = current_date_time.strftime("%A %B %d, %Y")
            table_data_list.insert(0,formatted_date_stamp)
            data_lists[symbol] = table_data_list 
        else:
            data_lists[symbol] = 'N/A'
            #### Print symbol and n/a for reference ####
            print symbol, "\tN/A"

    return data_lists

def add_labels(data_lists):
    """
Takes a dictionary with symbols for keys mapped to a list of statistic values.\
Returns a dictionary with symbols for keys mapped to a dictionary with the statistic label \
for keys, and the associated figure for the value. The new dictionary is returned
    """
    labeled_dictionary_collection = {}
    table_labels = ["Date Time Gathered","Market Cap (intraday)5","Enterprise Value 3",\
    "Trailing P/E (ttm, intraday)","Forward P/E 1","PEG Ratio (5 yr expected) 1","Price/Sales (ttm)",\
    "Price/Book (mrq)","Enterprise Value/Revenue (ttm) 3","Enterprise Value/EBITDA (ttm) 6",\
    "Fiscal Year Ends","Most Recent Quarter (mrq)","Profit Margin (ttm)","Operating Margin (ttm)",\
    "Return on Assets (ttm)","Return on Equity (ttm)","Revenue (ttm)","Revenue Per Share (ttm)",\
    "Qtrly Revenue Growth (yoy)","Gross Profit (ttm)","EBITDA (ttm) 6","Net Income Avl to Common (ttm)",\
    "Diluted EPS (ttm)","Qtrly Earnings Growth (yoy)","Total Cash (mrq)","Total Cash Per Share (mrq)",\
    "Total Debt (mrq)","Total Debt/Equity (mrq)","Current Ratio (mrq)","Book Value Per Share (mrq)",\
    "Operating Cash Flow (ttm)","Levered Free Cash Flow (ttm)","Beta","52-Week Change3",\
    "S&P500 52-Week Change3","52-Week High 3","52-Week Low 3","50-Day Moving Average 3",\
    "200-Day Moving Average 3","Avg Vol (3 month) 3","Avg Vol (10 day) 3","Shares Outstanding 5",\
    "Float","% Held by Insiders 1","% Held by Institutions 1","Shares Short 3","Short Ratio 3",\
    "Short % of Float 3","Shares Short (prior month) 3","Forward Annual Dividend Rate 4",\
    "Forward Annual Dividend Yield 4","Trailing Annual Dividend Yield 3","Trailing Annual Dividend Yield3",\
    "5 Year Average Dividend Yield 4","Payout Ratio 4","Dividend Date 3","Ex-Dividend Date 4",\
    "Last Split Factor 2","Last Split Date 3"]
    for symbol, data_list in data_lists.iteritems():
        labeled_dictionary_collection[symbol] = {label: stat for label in table_labels for stat in data_list}
    return labeled_dictionary_collection

def remove_number_symbols(data_lists):
    """
Takes a dictionary of symbols to lists filled with data, and looks for placeholder values,\ 
replacing them with the appropriate number value. The function then returns a new dictionary with the changes made.
    """
    billion = 'B'
    million = 'M'
    thousand = 'K'
    percent = '%'
    dot = '\.'
    comma = '\,'
    B = re.compile(billion)
    M = re.compile(million)
    K = re.compile(thousand)
    Perc = re.compile(percent)
    Dot = re.compile(dot)
    Comm = re.compile(comma)

    new_dictionary = {}
    for symbol, datalist in data_lists.iteritems():
        new_data_list = []
        if len(datalist) > 1:
            for statistic in datalist:
                if percent in statistic:
                    statistic = Perc.sub('', statistic)
                    new_data_list.append(float(statistic))
                if billion in statistic or million in statistic or thousand in statistic:
                    statistic = B.sub('0000000', statistic)
                    statistic = M.sub('00000', statistic)
                    statistic = K.sub('0', statistic)
                    statistic = Dot.sub('', statistic)
                    new_data_list.append(float(statistic))
                if comma in statistic:
                    statistic = Comm.sub('', statistic)
                    try:
                        statistic = float(statistic)
                    except:
                        pass
                    new_data_list.append(statistic)
                else:
                    try:
                        statistic = float(statistic)
                    except:
                        pass
                    new_data_list.append(statistic)
            new_dictionary[symbol] = new_data_list
        else:
            new_dictionary[symbol] = ['N/A']

    return new_dictionary

def get_quote(symbollist):
    """
Takes a list of symbols and uses ystockquote to request current stock information. \
Returns a dictionary with the keys as symbols, and the values being a dictionary of current stock
information. 
    """
    stock_dict = {}
    for symbol in symbollist:
        try:
            stock_dict[symbol] = ystockquote.get_all(ticker)
        else:
            stock_dict[symbol] = "N/A"
            print symbol, " Yahoo doesn't have this quote"
        return stock_dict


def get_d_prices(symbollist, country = "US"):
    """
Takes a list of symbols and uses the bloomberg api to get 4 minute stock information. \
Returns a dictionary with the keys as symbols, and the values as a list of tuples (timestamp, price).\
The default parameter for the country is US.
    """
    day_quote = {}
    for symbol in symbollist:
        url = "http://bloomberg.com/markets/chart/data/1D/" + symbol + ":" + country
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            data = json.load(resp)
            datapoints = data["data_values"]
            day_quote[symbol] = datapoints
        else:
            print symbol, "\tN/A"
            day_quote[symbol] = 'N/A'
    return day_quote

def get_m_prices(symbollist, country = "US"):
    """
Takes a list of symbols and uses the bloomberg api to get the monthly stock information. \
Returns a dictionary with the keys as symbols, and the values as a list of tuples (timestamp, price).\
The default parameter for the country is US.
    """
    month_quote = {}
    for symbol in symbollist:
        url = "http://bloomberg.com/markets/chart/data/1M/" + symbol + ":" + country
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            data = json.load(resp)
            datapoints = data["data_values"]
            month_quote[symbol] = datapoints
        else:
            print symbol, "\tN/A"
            day_quote[symbol] = 'N/A'
    return month_quote

def get_y_prices(symbollist, country = "US"):
    """
Takes a list of symbols and uses the bloomberg api to get yearly stock information. \
Returns a dictionary with the keys as symbols, and the values as a list of tuples (timestamp, price).\
The default parameter for the country is US.
    """
    year_quote = {}
    for symbol in symbollist:
        url = "http://bloomberg.com/markets/chart/data/1Y/" + symbol + ":" + country
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            data = json.load(resp)
            datapoints = data["data_values"]
            year_quote[symbol] = datapoints
        else:
            print symbol, "\tN/A"
            year_quote[symbol] = 'N/A'
    return year_quote

