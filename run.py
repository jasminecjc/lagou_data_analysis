import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from flask import *
import MySQLdb
import MySQLdb.cursors
import warnings
warnings.filterwarnings("ignore")
from config import *
import pprint

app = Flask(__name__)
app.config.from_object(__name__)

def connectdb():
	db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET)
	db.autocommit(True)
	cursor = db.cursor()
	return (db,cursor)

def closedb(db,cursor):
	db.close()
	cursor.close()

@app.route('/')
def index():
	return 'hello cjc'

@app.route('/tst')
def tst():
	return 'hello tst'

if __name__ == '__main__':
    app.run(debug=True)