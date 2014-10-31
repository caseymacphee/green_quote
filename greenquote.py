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
    "Date Time Gathered",
    "Market Cap (intraday)5",
    "Enterprise Value 3",
    "Trailing P/E (ttm, intraday)","PEG Ratio (5 yr expected) 1",
    "Profit Margin (ttm)",
    "Revenue (ttm)",
    "Gross Profit (ttm)",
    "EBITDA (ttm) 6",
    "Diluted EPS (ttm)",
    "Total Debt/Equity (mrq)",
    "Levered Free Cash Flow (ttm)",
    "52-Week Change3",
    "52-Week High 3",
    "52-Week Low 3",
    "50-Day Moving Average 3",
    "200-Day Moving Average 3",
    "% Held by Insiders 1",
    "% Held by Institutions 1",
    "Trailing Annual Dividend Yield 3",
    "Trailing Annual Dividend Yield3",
    "5 Year Average Dividend Yield 4",
    "Last Split Factor 2",
    "Last Split Date 3",]

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
    print "in get_company_entry with id=%s" % (id,)
    conn = get_database_connection()
    curs = conn.cursor()
    curs.execute('SELECT * from companies where index = {}'.format(id))
    values = curs.fetchall()
    return jsonify(dict(zip(table_labels, values)))

@app.route('/')
def show_indexes():
    return render_template('base.html')

@app.route('/lc/<id>')
def show_company_profile():
    # Flask doesn't support ':' in route, so underscore is passed in
    # but ':' is in the key
    id_pieces = id.split("_")
    id = (':').join(id_pieces)

    print "in_show_company_profile"
    query_result = get_company_entry(id)
    return query_result

if __name__ == '__main__':
	app.run(debug=True)
