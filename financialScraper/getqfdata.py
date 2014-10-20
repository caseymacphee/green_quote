import urllib
import re
import csv
import datetime
import pandas as pd


##Get some data and saving it to disk

symbolfile = open("Symbols.txt")
symbols = symbolfile.read()
symbolslist = symbols.split(",")
current_date = datetime.datetime.now()
formatted_datestamp = current_date.strftime("%A %B %d, %Y")
sustdata = open("dataFiles/G500-academic-data-sample-2012.csv", mode='r')
companydatalist = uncleaneddata.readlines()
sustdata.close()
for symbol in symbolslist:
    url = "http://finance.yahoo.com/q/ks?s={}+Key+Statistics".format(symbol)
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex = '<td class="yfnc_tabledata1">(.+?)</td>'
    data_table_pattern = re.compile(regex)

    financialstablelist = re.findall(data_table_pattern, htmltext)
    financialstablelist.insert(0,formatted_datestamp)
    
    outputfile = open("financial_data.csv","a")
    output = csv.writer(outputfile)
    output.writerow(financialstablelist)
    outputfile.close()

##declairing regex strings

regex1 = 'B'
regex2 = 'M'
regex3 = 'K'
regex4 = '%'
regex5 = '\.'
regex6 = '"<span id=""yfs_j10_'
regex7 = '</span>"'
regex8 = '"">'
regex9 = '\n'

###compiling regex strings

B = re.compile(regex1)
M = re.compile(regex2)
K = re.compile(regex3)
Perc = re.compile(regex4)
Dot = re.compile(regex5)
Span = re.compile(regex6)
Span1 = re.compile(regex7)
Span2 = re.compile(regex8)
Return = re.compile(regex9)

### reading from disk

uncleaneddata = open("financial_data.csv", mode='r+')
companydatalist = uncleaneddata.readlines()


cleaneddatafile = open("cleaned_financial_data.csv","a")

### substituting regex vals and writing to disk
for companydata in companydatalist:
    companydata = B.sub('0000000', companydata)
    companydata = M.sub('00000', companydata)
    companydata = K.sub('0', companydata)
    companydata = Perc.sub('', companydata)
    companydata = Span.sub('', companydata)
    companydata = Span1.sub('', companydata)
    companydata = Span2.sub(',', companydata)
    companydata = Dot.sub('', companydata)
    companydata = Return.sub('', companydata)

    cleaneddatafile.write(companydata)

cleaneddatafile.close()

#### reading from disk

readincleandata = pd.read_csv('cleaned_financial_data.csv', header=None)

### re-adjusting where periods were removed from float values in regex parse for percentages
i=0
while i < len(readincleandata[[13]]):
    number = readincleandata.ix[i,13]
    percentval = number/100
    readincleandata.ix[i,13] = percentval
    i+=1
i=0
while i < len(readincleandata[[28]]):
    number = readincleandata.ix[i,28]
    percentval = number/100
    readincleandata.ix[i,28] = percentval
    i+=1
i=0
while i < len(readincleandata[[34]]):
    number = readincleandata.ix[i,34] 
    percentval = number/100
    readincleandata.ix[i,34] = percentval
    i+=1

### copying a new dataframe with only the need to know figures
keystats = readincleandata[[1,2,3,13,17,28,32,34]]

meanrevenue = keystats[[17]].mean()
print meanrevenue


keystats.columns = ['Symbol','Market Cap (intraday)', 'Enterprise Value', 'Profit Margin %','Revenue Variance', 'Debt/Equity (mrq)', 'Levered Free Cash Flow (ttm)', '52-Week Change']
keystats.to_csv('key_stats.csv', sep =',', index = False, na_rep='N/A', header =True)




# elements  mrkt cap0, enterprise val 1, trailing pe 2,profit margin 11, debt to equity 25, current ratio 27, levered free cashflow 30,53



