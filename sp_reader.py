import collections
import psycopg2
import sys

# Define corporation records
CorpRecord = collections.namedtuple('CorpRecord', ('ticker', 'name'))
corp_record_list = []

# Connect to database
try:
    conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
except:
    print("Can't connect to the database")
cur = conn.cursor()

# Read rows from database
cur.execute("SELECT * FROM sp500;")
rows = cur.fetchall()
for row in rows:

    # Update tickers and name
    table = str.maketrans("", "", '\'.,')
    corp_name = row[1].translate(table)

    # Create record
    record = CorpRecord(ticker=row[0], name=corp_name)
    corp_record_list.append(record)

# Free database resources
cur.close()
conn.close()    
    
# Sort list of corporations
corp_record_list.sort(key=lambda x: x.ticker)

# Assemble strings
names = 'var names = ['
tickers = 'var tickers = ['
for record in corp_record_list:
    names += "\'" + record.name + ' (' + record.ticker + ")\', "
    tickers += "\'" + record.ticker + ' (' + record.name + ")\', "
names = names[:-2] + '];\n'
tickers = tickers[:-2] + '];\n'

# Open output file and write
outfile = open('C:\\Users\\zackh\\Google Drive\\business_stuff\\websites\\plutocracy\\new_plutocracy.js', 'w')
outfile.write(names)
outfile.write(tickers)

# Open program file
jsfile = open('program.js')
jsprogram = jsfile.read()
jsfile.close()
outfile.write(jsprogram)
outfile.close()