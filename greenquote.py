
import sys
from flask import Flask
sys.path.insert(0, "../financialScraper")
import financialScraper
import pandas
from sqlalchemy import create_engine

app = Flask(__name__)


@app.route('/')
def hello():
    engine = create_engine('postgresql://charlesgust@localhost/learning_journal')
    df = scraper()
    df.DataFrame.to_sql(name=entries, if_exists=replace, index=True)
    f = pandas.read_sql_query('SELECT * FROM entries', engine)
    return u"Everything Ran"

if __name__ == "__main__":
    app.run(debug=True)
