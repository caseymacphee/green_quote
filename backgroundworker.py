import sys
import os
sys.path.insert(0, "../financialScraper")
import pandas as pd
from financialScraper import getqf
from sqlalchemy import create_engine

running = True


# engine = create_engine(os.environ.get('DATABASE_URL'))

engine = create_engine('postgres://fkwfcpvbchmxps:VCmxue5WFWCOOHt56aqOm4FD_Z@ec2-54-83-205-46.compute-1.amazonaws.com:5432/d376d3nru8envq')
connection = engine.connect()
dfdict = getqf.scraper()
df = dfdict['nsdqct.csv']
df.to_sql(name='entries', con = connection, if_exists = 'replace')

connection.close()
