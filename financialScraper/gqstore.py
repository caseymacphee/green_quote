
from gevent.pool import Pool
import psycopg2
from flask import Flask, g

DB_SCHEMA = """
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    decorated_symbol TEXT PRIMARY KEY,    # aaaa:<exchange>:<country>
    title VARCHAR (127) NOT NULL,
    text TEXT NOT NULL,
    created TIMESTAMP NOT NULL
);
"""
DB_INSERT_ENTRY = """
INSERT INTO entries (title, text, created) VALUES (%s, %s, %s)
"""
DB_SELECT_ENTRIES_LIST = """
SELECT id, title, text, created FROM entries ORDER BY created DESC
"""
DB_SELECT_ENTRY = """
SELECT * FROM entries WHERE id = %s
"""
DB_UPDATE_ENTRY = """
UPDATE entries SET title = %s, text = %s WHERE id = %s
"""

app = Flask(__name__)
app.config['DATABASE'] = os.environ.get(
    'DATABASE_URL', 'dbname=gqscrapings user=charlesgust'
    )
# add the following two settings just below
app.config['ADMIN_USERNAME'] = os.environ.get(
    'ADMIN_USERNAME', 'admin'
)
app.config['ADMIN_PASSWORD'] = os.environ.get(
    'ADMIN_PASSWORD', pbkdf2_sha256.encrypt('admin')
)
app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'sooperseekritvaluenooneshouldknow'
)


class GQStore():
    def __init__():
        """ initialize the dabatase using DB_SCHEMA

        WARNING: executing this function will drop existing tables
        """
        with closing(connect_db()) as db:
            db.cursor().execute(DB_SCHEMA)
            db.commit()

    def connect_store():
        return psycopg2.connect(**DB_CONNECTION_PARAMS)

    def update_table(data):
        """
        given a table of data, add it to db or update db
        """



def open_gqstore():
    """
    return a connection to the green_quote database
    """
    return psycopg2.connect(**DB_CONNECTION_PARAMS)


