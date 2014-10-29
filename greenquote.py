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
	output = pd.read_sql_query('SELECT * FROM entries', engine)
	mean = output[[2]].mean()
	display_val = u"The mean is :" + str(mean)
	return display_val

@app.route('/')
def run():
	try:
		return load_data()
	except:
		return u'Loading... Come back later'
	

if __name__ == "__main__":
    app.run(debug=True)