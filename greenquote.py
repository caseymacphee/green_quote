import sys
import os
from flask import Flask
import pandas as pd
sys.path.insert(0, "../financialScraper")
from financialScraper import getqf
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['DATABASE'] = os.environ.get(
	'HEROKU_POSTGRESQL_GOLD_URL', ''
	)
dfdict = getqf.scraper()
engine = create_engine(app.config['DATABASE'])
@app.route('/')
def hello():
	df = dfdict['nsdqct.csv']
	df.to_sql(name='entries', con = engine, if_exists = 'replace')
	output = pd.read_sql_query('SELECT * FROM entries', engine)
	mean = output[[2]].mean()
	return u"The mean is :" + str(mean)

if __name__ == "__main__":
    app.run(debug=True)
