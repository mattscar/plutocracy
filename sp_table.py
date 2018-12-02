# Declarations
table_dec = 'CREATE TABLE sp500 (ticker varchar(8) CONSTRAINT firstkey PRIMARY KEY, name varchar(50) NOT NULL, sector sector_type NOT NULL, subsector subsector_type NOT NULL);'

# Sets of elements
sector_set = set()
subsector_set = set()

# Read sectors and subsectors from file
with open('sp_list.txt', 'r') as infile:

    # Iterate through lines
    lines = infile.readlines()
    for line in lines:
    
        # Read text after 'reports'
        pos = line.index('reports') + 8
        endLine = line[pos:]
        
        tokens = endLine.split("\t")
        sector_set.add(tokens[0].strip())
        subsector_set.add(tokens[1].strip())

    infile.close()  

# Update sector declaration
sector_dec = 'CREATE TYPE sector_type AS ENUM ('
for sec in sector_set:
    sector_dec += "\'" + sec + "\', "
sector_dec = sector_dec[:-2] + ');'

# Update subsector declaration
subsector_dec = 'CREATE TYPE subsector_type AS ENUM ('
for subsec in subsector_set:
    subsector_dec += "\'" + subsec + "\', "
subsector_dec = subsector_dec[:-2] + ');'    

# Open output file and write
outfile = open('create_table.sql', 'w')
outfile.write(sector_dec)
outfile.write('\n\n')
outfile.write(subsector_dec)
outfile.write('\n\n')
outfile.write(table_dec)