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

        pos = line.index('reports') - 1
        startLine = line[:pos]

        tokens = startLine.split()
        ticker = tokens[0]

        # Determine company name
        name = ''
        for i in range(1, len(tokens)):
            name += tokens[i] + ' '
        name = name.strip()

        # Determine sector and subsector
        endLine = line[pos+9:]
        tokens = endLine.split("\t")
        sector = tokens[0].strip()
        subsector = tokens[1].strip()

        # Insert values into table
        cur.execute("INSERT INTO sp500 (ticker, name, sector, subsector) VALUES (%s, %s, %s, %s)", (ticker, name, sector, subsector))
        conn.commit()

# Free database resources
cur.close()
conn.close()