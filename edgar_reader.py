from bs4 import BeautifulSoup
import datetime
import psycopg2
import requests
import sys

def convert_date(date_str):
    report_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return report_date

def check_str(val_str):
    if val_str.find('.') != -1:
        return str(int(float(val_str)))
    else:
        return val_str
    
# Set initial parameters
type = '10-Q'
early_date = datetime.datetime.strptime('2013-01-28', '%Y-%m-%d')
base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}"

# Connect to database
try:
    conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
except:
    print("Can't connect to the database")
cur = conn.cursor()

# Start company
start_company = 'ARNC'
cont = True

# Access S&P records and iterate
cur.execute('SELECT * FROM sp500;')
stock_list = cur.fetchall()
for idx, stock_record in enumerate(stock_list):

    if cont:
        if stock_record[0] != start_company:
            continue
        else:
            cont = False

    # Set table name
    table_name = stock_record[0].replace('.', '_').lower() + '_fund'
    cik = stock_record[4]

    # Print debug data
    print(table_name + ", " + str(idx))
    print(base_url.format(cik, type))

    # Obtain HTML for search page
    edgar_resp = requests.get(base_url.format(cik, type))
    edgar_str = edgar_resp.text

    # Find the document link
    doc_link = ''
    soup = BeautifulSoup(edgar_str, 'html.parser')
    table_tag = soup.find('table', class_='tableFile2')
    rows = table_tag.find_all('tr')

    for index, row in enumerate(rows):
        cells = row.find_all('td')
        if len(cells) > 3 and cells[0].text == type:

            # Check report date
            date = convert_date(cells[3].text)
            if date < early_date:
                break

            # Access the report
            doc_link = 'https://www.sec.gov' + cells[1].a['href']
            if doc_link == '':
                print("Couldn't find the document link")
                sys.exit()

            # print(doc_link)

            # Obtain HTML for document page
            doc_resp = requests.get(doc_link)
            doc_str = doc_resp.text

            # Find the XBRL link
            xbrl_link = ''
            soup = BeautifulSoup(doc_str, 'html.parser')
            table_tag = soup.find('table', class_='tableFile', summary='Data Files')
            if table_tag == None:
                continue

            # Iterate through XBRL-related documents
            xbrl_rows = table_tag.find_all('tr')
            for xbrl_row in xbrl_rows:
                xbrl_cells = xbrl_row.find_all('td')
                if len(xbrl_cells) > 3:
                    if '.INS' in xbrl_cells[3].text:

                        # Get link to XBRL document
                        xbrl_link = 'https://www.sec.gov' + xbrl_cells[2].a['href']
                        xbrl_resp = requests.get(xbrl_link)
                        xbrl_str = xbrl_resp.text

                        # Search for fields
                        soup = BeautifulSoup(xbrl_str, 'lxml')
                        tag_list = soup.find_all()
                        report_date = date.strftime('%Y-%m-%d')
                        assets = ''
                        liabilities = ''
                        cash = ''
                        debt = ''

                        for tag in tag_list:

                            if tag.name == 'us-gaap:assets' and tag.text != '':
                                assets = tag.text

                            if tag.name == 'us-gaap:liabilities' and tag.text != '' and tag.text != '0':
                                liabilities = tag.text

                            if tag.name == 'us-gaap:cash' and tag.text != '' and tag.text != '0':
                                cash = tag.text

                            if tag.name == 'us-gaap:debt' and tag.text != '' and tag.text != '0':
                                debt = tag.text

                        if assets == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:assetscurrent' and tag.text != '':
                                    assets = tag.text

                        if liabilities == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:liabilitiescurrent' and tag.text != '':
                                    liabilities = tag.text

                        if cash == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:cashcashequivalentsandshortterminvestments' and tag.text != '' and tag.text != '0':
                                    cash = tag.text
   
                        if cash == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:cashandcashequivalentsatcarryingvalue' and tag.text != '':
                                    cash = tag.text

                        if cash == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:cashandcashequivalentsatcarryingvalueincludingdiscontinuedoperations' and tag.text != '' and tag.text != '0':
                                    cash = tag.text

                        if cash == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:cashandduefrombanks' and tag.text != '' and tag.text != '0':
                                    cash = tag.text

                        if cash == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:cashequivalentsatcarryingvalue' and tag.text != '' and tag.text != '0':
                                    cash = tag.text                                    

                        if cash == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:cashcashequivalentsrestrictedcashandrestrictedcashequivalents' and tag.text != '' and tag.text != '0':
                                    cash = tag.text       
                                   
                        if debt == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:debtcurrent' and tag.text != '' and tag.text != '0':
                                    debt = tag.text

                        if debt == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:debtandcapitalleaseobligations' and tag.text != '' and tag.text != '0':
                                    debt = tag.text

                        if debt == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:longtermdebt' and tag.text != '' and tag.text != '0':
                                    debt = tag.text

                        if debt == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:longtermdebtcurrent' and tag.text != '' and tag.text != '0':
                                    debt = tag.text

                        if debt == '':
                            for tag in tag_list:
                                if tag.name == 'us-gaap:longtermdebtnoncurrent' and tag.text != '' and tag.text != '0':
                                    debt = tag.text

                        if debt == '':
                            debt = '-1'
                            
                        if liabilities == '':
                            liabilities = '-1'
                            
                        # Insert record into database
                        cmd = 'INSERT INTO ' + table_name + ' (report_date, assets, liabilities, cash, debt) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
                        cur.execute(cmd, (report_date, check_str(assets), check_str(liabilities), check_str(cash), check_str(debt)))
                        conn.commit()

# Free database resources
cur.close()
conn.close()