import collections
import psycopg2
import requests
import sys
from six.moves import urllib
import json

from bs4 import BeautifulSoup

# Declare named tuple
CorpRecord = collections.namedtuple('CorpRecord', ('ticker', 'name', 'sector', 'subsector', 'cik'))
corp_record_list = []

# Function for printing
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

# Connect to database
try:
    conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
except:
    print("Can't connect to the database")
cur = conn.cursor()

# Get existing ticker list
old_list = set()
cur.execute("SELECT * FROM sp500;")
rows = cur.fetchall()
for row in rows:
    old_list.add(row[0])

# Access Wikipedia page
req = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
soup = BeautifulSoup(req.content, 'lxml')
sp_table = soup.find("table", {"class": ["sortable"]})
table_rows = sp_table.findAll("tr")

# Get list of tickers from Wikipedia
new_list = set()
for row in table_rows:

    cols = row.findAll("td")
    if len(cols):

        # Ticker symbol
        ticker_col = cols[0]
        if ticker_col is not None:
            corp_ticker = ticker_col.a.text.strip()
            new_list.add(corp_ticker)
            if corp_ticker not in old_list:

                # Company name
                name_col = cols[1]
                if name_col is not None:
                    corp_name = name_col.text.strip()

                # Sector name
                sector_col = cols[3]
                if sector_col is not None:
                    sector_name = sector_col.text.strip()

                # Subsector name
                subsector_col = cols[4]
                if subsector_col is not None:
                    subsector_name = subsector_col.text.strip()
                    if subsector_name == "Data Processing & Outsources Services":
                        subsector_name = "Data Processing & Outsourced Services"

                # CIK code
                cik_col = cols[7]
                if cik_col is not None:
                    cik_code = cik_col.text.strip()

                # Create record
                record = CorpRecord(ticker=corp_ticker, name=corp_name,
                    sector=sector_name, subsector=subsector_name, cik=cik_code)
                corp_record_list.append(record)

# Delete old tickers
bad_tickers = list(old_list - new_list)
if len(bad_tickers) > 0:
    for bad_ticker in bad_tickers:
        print('Deleting ' + bad_ticker)
        cmd = 'DELETE FROM sp500 WHERE ticker = %s;'
        cur.execute(cmd, (bad_ticker,))
        ticker = bad_ticker.lower() + '_stock'
        cmd = "DROP TABLE " + ticker + ";"
        cur.execute(cmd, (ticker,))
    conn.commit()

# Create tables for new tickers
if len(corp_record_list) > 0:
    for corp_record in corp_record_list:

        # Add entry to sp500 table
        cmd = 'INSERT INTO sp500 (ticker, name, sector, subsector, cik_code) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
        cur.execute(cmd, (corp_record.ticker, corp_record.name, corp_record.sector, corp_record.subsector, corp_record.cik))

        # Create table
        table_name = corp_record.ticker.lower().replace('.', '_') + '_stock'        
        cmd = "CREATE TABLE " + table_name;
        cmd += " (stock_date DATE PRIMARY KEY, high NUMERIC(10, 4) NOT NULL, low NUMERIC(10, 4) NOT NULL, volume INTEGER NOT NULL, change_percent REAL NOT NULL, vwap NUMERIC(10, 4) NOT NULL);"
        cur.execute(cmd)

        # Get stock data
        url = 'https://api.iextrading.com/1.0/stock/' + corp_record.ticker + '/chart/5y'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        result_json = resp.read().decode('utf-8')
        record_list = json.loads(result_json)
        
        # Insert stock data into table
        for record in record_list:

            if 'date' in record and 'high' in record and 'low' in record and 'volume' in record and 'changePercent' in record and 'vwap' in record: 
                stock_date = record['date']
                high = record['high']
                low = record['low']
                volume = record['volume']
                change_percent = record['changePercent']
                vwap = record['vwap']
                cmd = 'INSERT INTO ' + table_name + ' (stock_date, low, high, volume, change_percent, vwap) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
                cur.execute(cmd, (stock_date, low, high, volume, change_percent, vwap))
                
        conn.commit()

# Free database resources
cur.close()
conn.close()