import sys
import os
sys.path.insert(0, "../financialScraper")
import pandas as pd
from financialScraper import getqf
from sqlalchemy import create_engine

running = True


engine = create_engine(os.environ.get('DATABASE_URL'))
while running:
	companies_data_frame, stats_data_frame = getqf.scraper()
	companies_data_frame.to_sql(name='companies', con = engine, if_exists = 'replace')
	stats_data_frame.to_sql(name='stats', con = engine, if_exists = 'replace')


