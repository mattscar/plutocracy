from six.moves import urllib
import json
import psycopg2
import sys

# Connect to database
try:
    conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
except:
    print("Can't connect to the database")
cur = conn.cursor()

# Read sectors and subsectors from file
with open('sp_list.txt', 'r') as infile:

    # Iterate through lines
    lines = infile.readlines()
    for line in lines:

        # Determine ticker symbol
        pos = line.index('reports') - 1
        startLine = line[:pos]
        tokens = startLine.split()
        ticker = tokens[0].lower()
        table_name = tokens[0].replace('.', '_') + '_T'

        # Send HTTP request
        url = 'https://api.iextrading.com/1.0/stock/' + ticker + '/chart/5y'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)

        # Convert response to Python list of dicts
        result_json = resp.read().decode('utf-8')
        record_list = json.loads(result_json)

        # Iterate through list
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