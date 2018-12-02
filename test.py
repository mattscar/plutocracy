import psycopg2

# Connect to database
try:
    conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
except:
    print("Can't connect to the database")
cur = conn.cursor()

cur.execute('SELECT * FROM sp500;')
for record in cur:
    print(record[0])

# Free database resources
cur.close()
conn.close()
