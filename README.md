green_quote
===========
Co-Collaborators Charles Gust, and Casey MacPhee

A financial, and stock analysis tool for the eco-minded. The stock quote scraping is done with a third party library 'ystockquote' created by Corey Goldberg (2007,2008,2013) using Yahoo Finance. The data set for this implementation includes the New York Stock Exchange Energy Index, the Nasdaq Energy Index, the NASDAQ® Clean Edge® Green Energy Index, the Oil & Gas Companies Listed on Toronto Stock Exchange, and TSX Venture Exchange, and the Renewable Energy and Clean Technology Companies Listed on TSX, and TSXV.  Additional historical stock information is gathered with the Bloomberg API. Quarterly financial information is scraped from Yahoo finance. The script getqf.py provides functionality for gathering this information. The main building block for these functions are lists of symbols, and there is functionality for reading in csv files into that structure.

The flask application provides the front end functionality for the client side.