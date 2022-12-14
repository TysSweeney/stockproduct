from github import Github
import bitdotio
import csv

# Log into GitHub & Connect to Repo
token = #token
g = Github(token)
repo = g.get_repo("TysSweeney/stockproduct")

# Establish SQL connection
# Connect to bit.io
b = bitdotio.bitdotio(#password)

# Connect to the database
conn = b.get_connection("tyssweeney/stockproduct")
cursor = conn.cursor()

# List file names and PythonAnywhere locations
files = [
    ["'KMB'",'kmb.csv','/home/tyssweeney/kmb.csv'],
    ["'COCO'",'coco.csv','/home/tyssweeney/coco.csv'],
    ["'PG'",'pg.csv','/home/tyssweeney/pg.csv']
    ]

# Initiate header list for CSV files
headerlist = ["DATE","COMPANY","PRODUCT","TICKER","PRODUCT PRICE","SHARE PRICE","PRODUCT % CHANGE","SHARE % CHANGE"]

# Initiate empty data passthrough variable
data = ""

# Update CSV Files in PythonAnywhere and GitHub
for file in files:

    # Clear data passthrough variable
    data = ""

    # Write CSV update in PythonAnywhere
    with open(file[2], 'w', newline='',encoding='utf-8') as f:
        fwriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cursor.execute("SELECT pp.date::date, company_name, product_name, ticker, pp.price, s.price, pp.pct_change, s.pct_change FROM product_prices as pp INNER JOIN products as p ON pp.product_id = p.product_id INNER JOIN companies as c ON c.company_id = p.company_id INNER JOIN stocks as s ON c.company_id = s.company_id AND s.date::date = pp.date::date WHERE ticker =" +file[0]+" ORDER BY pp.date")
        table = cursor.fetchall()
        fwriter.writerow(headerlist)
        for row in table:
            fwriter.writerow(row)
            print(row)
    f.close()

    # Read CSV into data passthrough variable
    with open(file[2], newline='',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            for element in row:
                if row.index(element) == len(row)-1:
                    data = data + str(element)
                else:
                    data = data + str(element) + ","
            data = data + "\n"
    f.close()

    # Update file in GitHub
    file = repo.get_contents(file[1])
    repo.update_file(file.path, "Python AutoUpdate", data, file.sha, branch="main")
