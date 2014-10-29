import sys
import os
sys.path.insert(0, "../financialScraper")
import pandas as pd
from financialScraper import getqf
from sqlalchemy import create_engine

running = True

while running:
	engine = create_engine(os.environ.get('DATABASE_URL'))
	dfdict = getqf.scraper()
	df = dfdict['nsdqct.csv']
	df.to_sql(name='entries', con = engine, if_exists = 'replace')
