import os
from flask import Flask
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['DATABASE'] = os.environ.get(
	'DATABASE_URL', ''
	)

engine = create_engine(app.config['DATABASE'])

def load_data():
	companies_data_frame = pd.read_sql_query('SELECT * FROM companies', engine)
	stats_data_frame = pd.read_sql_query('SELECT * FROM stats', engine)
	return "Companies loaded!"

@app.route('/')
def run():
	try:
		return load_data()
	except:
		return u'Loading... Come back later'
	

if __name__ == "__main__":
    app.run(debug=True)