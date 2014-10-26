#!/usr/bin/env python

import urllib2
import re
import csv
import datetime
import pandas as pd
import ystockquote
from bs4 import BeautifulSoup
import json
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
        name = name.split(csvdelim)
        index_lists[name[0]] = symbol_list
    return index_lists


def get_data(symbollist, ext = ''):
    """
Takes a list of symbols, and requests the key statistics page from yahoo for that company. \
Searches for all the table data for that company and returns a dictionary of symbols for keys mapped to\
a list of statistical data for that information.
    """
    data_lists = {}
    for symbol in symbollist:
        url = "http://finance.yahoo.com/q/ks?s={}+Key+Statistics".format(symbol + ext)
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            htmltext = BeautifulSoup(resp.read())
            data_table_pattern = "yfnc_tabledata1"
            result_set = htmltext.findAll(class_= data_table_pattern)
            table_data_list = []
            for stat in result_set:
                table_data_list.append(stat.get_text())
            current_date_time = datetime.datetime.now()
            formatted_date_stamp = current_date_time.strftime("%A %B %d, %Y")
            if len(table_data_list) == 0:
                print symbol 
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

def get_quote(symbollist, ext = ''):
    """
Takes a list of symbols and uses ystockquote to request current stock information. \
Returns a dictionary with the keys as symbols, and the values being a dictionary of current stock
information. 
    """
    stock_dict = {}
    for symbol in symbollist:
        try:
            stock_dict[symbol] = ystockquote.get_all(symbol+ext)
        except:
            stock_dict[symbol] = "N/A"
            print symbol, " Yahoo doesn't have this quote"
    return stock_dict


def get_d_prices(symbollist, country = "US"):
    """
Takes a list of symbols and uses the bloomberg api to get 4 minute stock information. \
Returns a dictionary with the keys as symbols, and the values as a list of tuples (timestamp, price).\
The default parameter for the country is US.
    """
    dash = '-'
    to_slash = re.compile(dash)
    day_quote = {}
    for symbol in symbollist:
        symbol = to_slash.sub('/', symbol)
        print symbol
        url = "http://bloomberg.com/markets/chart/data/1D/{}:{}".format(symbol,country)
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
    dash = '-'
    to_slash = re.compile(dash)
    month_quote = {}
    for symbol in symbollist:
        symbol = to_slash.sub('/', symbol)
        print symbol
        url = "http://bloomberg.com/markets/chart/data/1M/{}:{}".format(symbol,country)
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            data = json.load(resp)
            datapoints = data["data_values"]
            month_quote[symbol] = datapoints
        else:
            print symbol, "\tN/A"
            month_quote[symbol] = 'N/A'
    return month_quote

def get_y_prices(symbollist, country = "US"):
    """
Takes a list of symbols and uses the bloomberg api to get yearly stock information. \
Returns a dictionary with the keys as symbols, and the values as a list of tuples (timestamp, price).\
The default parameter for the country is US.
    """
    dash = '-'
    to_slash = re.compile(dash)
    year_quote = {}
    for symbol in symbollist:
        symbol = to_slash.sub('/', symbol)
        print symbol
        url = "http://bloomberg.com/markets/chart/data/1Y/{}:{}".format(symbol,country)
        resp = urllib2.urlopen(url)
        if resp.getcode() == 200:
            data = json.load(resp)
            datapoints = data["data_values"]
            year_quote[symbol] = datapoints
        else:
            print symbol, "\tN/A"
            year_quote[symbol] = 'N/A'
    return year_quote

def main():
    indexlist = []
    indexlist.append('dataFiles/nsdqctsymbols.csv')
    indexlist.append('dataFiles/nsdqesymbols.csv')
    indexlist.append('dataFiles/nyesymbols.csv')
    indexlist.append('dataFiles/tsxogsymbols.csv')
    indexlist.append('dataFiles/tsxctsymbols.csv')
    indexlist.append('dataFiles/tsxvctsymbols.csv')
    indexlist.append('dataFiles/tsxvogsymbols.csv')


    indexlist = load_files(indexlist)

    day_quotes = {}
    for index, symbollist in indexlist.iteritems():
        if index == 'nsdqctsymbols.csv' or index == 'nsdqesymbols.csv' or index == 'nyesymbols.csv':
            day_quotes[index] = get_d_prices(symbollist)
        else:
            day_quotes[index] = get_d_prices(symbollist, "CN")

    month_quotes = {}
    for index, symbollist in indexlist.iteritems():
        if index == 'nsdqctsymbols.csv' or index == 'nsdqesymbols.csv' or index == 'nyesymbols.csv':
            month_quotes[index] = get_m_prices(symbollist)
        else:
            month_quotes[index] = get_m_prices(symbollist, "CN")

    year_quotes = {}
    for index, symbollist in indexlist.iteritems():
        if index == 'nsdqctsymbols.csv' or index == 'nsdqesymbols.csv' or index == 'nyesymbols.csv':
            year_quotes[index] = get_y_prices(symbollist)
        else:
            year_quotes[index] = get_y_prices(symbollist, "CN")

    qfindexdict = {}
    for index, symbollist in indexlist.iteritems():
        print index
        if index == 'tsxvctsymbols.csv' or index == 'tsxvogsymbols.csv':
            qfindexdict[index] = get_data(symbollist, '.V')
        elif index == 'tsxctsymbols.csv' or index == 'tsxogsymbols.csv':
            qfindexdict[index] = get_data(symbollist, '.TO')
        else:
            qfindexdict[index] = get_data(symbollist)

    current_quotes = {}
    for index, symbollist in indexlist.iteritems():
        print index
        if index == 'tsxvctsymbols.csv' or index == 'tsxvogsymbols.csv':
            current_quotes[index] = get_quote(symbollist, '.V')
        elif index == 'tsxctsymbols.csv' or index == 'tsxogsymbols.csv':        
            current_quotes[index] = get_quote(symbollist, '.TO')
        else:
            current_quotes[index] = get_quote(symbollist)

    fltpointmarketdicts = {}
    for index, companydict in qfindexdict.iteritems():
        fltpointmarketdicts[index] = remove_number_symbols(companydict)

    labeledindexdicts = {}
    for index, companydict in qfindexdict.iteritems():
        labeledindexdicts[index] = add_labels(companydict)

    return fltpointmarketdicts, labeledindexdicts, current_quotes, day_quotes, month_quotes, year_quotes
if __name__ == '__main__':
    fltpntdict, lbldict, currdict, year, month, day = main()
