# Open output file and write
outfile = open('corp_tables.sql', 'w')

# Read sectors and subsectors from file
with open('sp_list.txt', 'r') as infile:

    # Iterate through lines
    lines = infile.readlines()
    for line in lines:
    
        # Read ticker
        pos = line.index('reports') - 1
        startLine = line[:pos]

        tokens = startLine.split()
        ticker = tokens[0].replace('.', '_') + '_T'
        ticker = ticker.lower()
        table_name = tokens[0].replace('.', '_').lower() + '_fund'
        str = 'CREATE TABLE ' + table_name + ' (report_date date PRIMARY KEY, assets bigint, liabilities bigint, cash bigint, debt bigint);\n'
        # str = 'DROP TABLE ' + table_name + ';\n'
        # str = 'ALTER TABLE ' + ticker + ' RENAME TO ' + new_ticker + ';\n'
        outfile.write(str)

    infile.close()  
outfile.close()