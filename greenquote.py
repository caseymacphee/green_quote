import sys
import os
from threading import Thread
from flask import Flask
import pandas as pd
sys.path.insert(0, "../financialScraper")
from financialScraper import getqf
#from sqlalchemy import create_engine

app = Flask(__name__)
# app.config['DATABASE'] = os.environ.get(
# 	'HEROKU_POSTGRESQL_GOLD_URL', ''
# 	)
# engine = create_engine(app.config['DATABASE'])

display_val = u"Loading data..."

# def load_data():
# 	dfdict = getqf.scraper()
# 	df = dfdict['nsdqct.csv']
# 	df.to_sql(name='entries', con = engine, if_exists = 'replace')
# 	output = pd.read_sql_query('SELECT * FROM entries', engine)
# 	mean = output[[2]].mean()
# 	display_val = u"The mean is :" + str(mean)

# thread1 = Thread(target = load_data)
# thread1.start()

@app.route('/')
def hello():
	return display_val
	

if __name__ == "__main__":
    app.run(debug=True)
