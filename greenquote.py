import os
from flask import Flask
from flask import g
from flask import jsonify
import psycopg2
import json
from json import load
from flask import render_template
app = Flask(__name__)

app.config['DATABASE'] = os.environ.get(
	'DATABASE_URL', ''
	)

app.config['SECRET_KEY'] = os.environ.get(
	'FLASK_SECRET_KEY', '892BEF232E4A81DA955BA79D42E9D'
	)

table_labels = [
    "Universal Stock Symbol",
    "Current Price",
    "Num Change",
    "% Change",
    "Universal Stock Symbol",
    "Date Time Gathered",
    "Market Cap (intraday)",
    "Enterprise Value",
    "Trailing P/E (ttm, intraday)","PEG Ratio (5 yr expected)",
    "Profit Margin (ttm)",
    "Revenue (ttm)",
    "Gross Profit (ttm)",
    "EBITDA (ttm)",
    "Diluted EPS (ttm)",
    "Total Debt/Equity (mrq)",
    "Levered Free Cash Flow (ttm)",
    "52-Week Change",
    "52-Week High",
    "52-Week Low",
    "50-Day Moving Average",
    "200-Day Moving Average",
    "% Held by Insiders",
    "% Held by Institutions",
    "Trailing Annual Dividend Yield",
    "Trailing Annual Dividend Yield %",
    "5 Year Average Dividend Yield",
    "Last Split Factor",
    "Last Split Date"]

def connect_db():
	return psycopg2.connect(app.config['DATABASE'])

def get_database_connection():
	db = getattr(g, 'db', None)
	if db is None:
		g.db = db = connect_db()
	return db

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		if exception and isinstance(exception, psycopg2.Error):
			#if there's a problem with the databse rollback the transaction
			db.rollback()
		else:
			db.commit()
		db.close()


def get_company_entry(id):
    conn = get_database_connection()
    curs = conn.cursor()
    curs.execute("SELECT * from quotes where index = '{}'".format(id))
    quotes = curs.fetchall()

    curs.execute("SELECT * from companies where index = '{}'".format(id))
    statistics = curs.fetchall()

    vlist = []
    for value in quotes[0]:
        vlist.append(value)
    for value in statistics[0]:
        vlist.append(value)

    zip_tablevalues = zip(table_labels, vlist) # should be list of tuples
    tojson = dict(zip_tablevalues)
    return jsonify(tojson)

@app.route('/')
def show_indexes():
    return render_template('base.html')

@app.route('/lc/<id>')
def show_company_profile(id):
    # Flask doesn't support ':' in route, so underscore is passed in
    # but ':' is in the key
    id_pieces = id.split("_")
    id = (':').join(id_pieces)

    query_result = get_company_entry(id)
    return query_result

if __name__ == '__main__':
	app.run(debug=True)
