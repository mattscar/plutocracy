import psycopg2

try:
    conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
except:
    print("I can't connect to the database")

# Obtain cursor
cur = conn.cursor()

# Read sectors and subsectors from file
with open('sp_list.txt', 'r') as infile:

    # Iterate through lines
    lines = infile.readlines()
    for line in lines:

        tokens = line.split()
        ticker = tokens[0]

        # Determine CIK code
        cik_code = tokens[-1]    
        
        # Update table rows
        cur.execute("UPDATE sp500 SET cik_code=(%s) WHERE ticker = (%s)", (cik_code, ticker));
        conn.commit()

# Free database resources
cur.close()
conn.close()