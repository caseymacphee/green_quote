import re
import json
import json.dump

def load_files(symbolfilepaths, csvdelim = "\n"):
    """ 
Takes a list of symbol file paths to respective csv files, and loads their content into a \
dictionary of file-paths to lists containing the content of the csv. The delimeter of the csv files \
defaults to a ','. 
    """
    fileattribute = 'symcomp.csv'
    symcomp = re.compile(fileattribute)
    index_lists = {}
    for file in symbolfilepaths:
    	path = file.split('/')
        name = path[len(path)-1]
        name = symcomp.sub('', name)
        symbol_file = open(file)
        symbol_string = symbol_file.read()
        symbol_file.close()
        symbol_list = symbol_string.split(csvdelim)
        index_dict = {}
        for symbol_chunk in symbol_list:
        	if name == 'nsdqe' or name == 'nsdqct':
	        	symbol, company = symbol_chunk.split('","')
	        	index_dict[symbol] = [symbol +':'+ name, company]
	        else:
	        	company, symbol = symbol_chunk.split('","')
	        	index_dict[symbol] = [symbol +':'+ name, company]  
        index_lists[name] = index_dict
    with open("masterjsonobject.json", 'w') as outfile:
        json.dump(index_lists, outfile, indent= 4)

data_files = ['dataFiles/nsdqctsymcomp.csv', 'dataFiles/nsdqesymcomp.csv', 'dataFiles/nyesymcomp.csv','dataFiles/tsxctsymcomp.csv', 'dataFiles/tsxogsymcomp.csv', 'dataFiles/tsxvctsymcomp.csv', 'dataFiles/tsxvogsymcomp.csv']
