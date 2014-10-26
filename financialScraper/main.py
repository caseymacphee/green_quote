from getqf import *

indexlist = []
indexlist.append('dataFiles/nsdqctsymbols.csv')
indexlist.append('dataFiles/nsdqesymbols.csv')
indexlist.append('dataFiles/nyesymbols.csv')
indexlist.append('dataFiles/tsxogsymbols.csv')
indexlist.append('dataFiles/tsxctsymbols.csv')
indexlist.append('dataFiles/tsxvctsymbols.csv')
indexlist.append('dataFiles/tsxvogsymbols.csv')


marketlist = load_files(indexlist)
marketdict = {}
for index, symbollist in marketlist.iteritems():
    print index
    marketdict[index] = get_data(symbollist)

fltpointmarketdicts = {}
for index, companydict in marketdict.iteritems():
	fltpointmarketdicts[index] = remove_number_symbols(companydict)

labeledmarketdicts = {}
for index, companydict in marketdict.iteritems():
	labeledmarketdicts[index] = add_labels(companydict)