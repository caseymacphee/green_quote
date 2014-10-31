import sys
import os
sys.path.insert(0, "../financialScraper")
import pandas as pd
from financialScraper import getqf
from financialScraper import get_quote
from sqlalchemy import create_engine
import threading
import time

running = True
engine = create_engine(os.environ.get('DATABASE_URL'))


def quotes():
	while running:
		current_quotes = get_quote.current_quote()
		current_quotes.to_sql(name= 'quotes', con = engine, if_exists = 'replace')

quotes = threading.Thread(target = quotes)
quotes.start()

while running:
	time.sleep(3600)
	companies_data_frame, stats_data_frame = getqf.scraper()
	companies_data_frame.to_sql(name='companies', con = engine, if_exists = 'replace')
	stats_data_frame.to_sql(name='stats', con = engine, if_exists = 'replace')


