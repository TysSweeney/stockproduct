import requests
import json
import bitdotio
from pprint import pprint
import yfinance as yf
from datetime import date

# Establish SQL connection
# Connect to bit.io
b = bitdotio.bitdotio(#password)

# Connect to the database
conn = b.get_connection("tyssweeney/stockproduct")
cursor = conn.cursor()

# Amazon's API returns a price as a solid integer without separating
# dollars from cents. This function returns a floating point number.

def decimal_conversion(priceAmazon):
    print("Price is: " + str(priceAmazon))

    if type(priceAmazon) != int:
        raise ValueError('Not an integer.')

    else:
        stringify = str(priceAmazon)

        num_length = len(str(priceAmazon))
        right_index = num_length - 2

        dollars = stringify[:right_index]
        cents = stringify[-2:]

        combined = dollars + "." + cents
        price = float(combined)

        return price

# API get function for Amazon price for Kleenex Expressions Soothing
# Lotion Facial Tissues with Coconut Oil, Aloe & Vitamin E

def get_price(asin):

    # Set URL and intake Amazon ASIN
    url = "https://amazon-price1.p.rapidapi.com/priceReport"
    querystring = {"asin":asin,"marketplace":"US"}

    headers = {
    	"X-RapidAPI-Key": #key,
    	"X-RapidAPI-Host": #host
    }

    # Make the API request and parse as JSON
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.text
    parse_json = json.loads(data)

    # Extract price from JSON and return it
    priceAmazon = parse_json['prices']['priceAmazon']
    return priceAmazon

# Cycle through existing products and return a list of IDs and ASINs

def product_cycle():
    # Returns a dictionary of IDs and ASINs
    product_info = {}
    cursor.execute("SELECT product_id,amazon_asin FROM products")

    table = cursor.fetchall()

    # Print check
    #print("Product Cycle")

    for row in table:

        # Princt check
        pprint(row)

        # Unpacking
        (pid, asin) = row
        product_info.update({pid:asin})

    return product_info

# Collect current prices and input them into products
# SQL table on bit.io

def load_price():

    product_dict = product_cycle()

    for product_id in product_dict:

        # Print check
        #print(product_id)
        #print(product_dict[product_id])

        pid = str(product_id)

        # Get the price for the current product
        price = decimal_conversion(get_price(product_dict[product_id]))

        cursor.execute("SELECT price FROM product_prices WHERE product_id = " + pid +" ORDER BY date desc LIMIT 1")
        prod_last_price = float(cursor.fetchall()[0][0])

        pct_change = str(round((price - prod_last_price) / prod_last_price,4))

        sprice = str(price)
        cursor.execute('''
                INSERT INTO product_prices(date,price,product_id,pct_change)
                VALUES ( NOW(),'''+sprice+","+pid+","+pct_change+");")

    conn.commit()
    #print("Completed.")

# This function gets the current stock price of a ticker via yfinance

def get_stock_price(ticker):

    stock = yf.Ticker(ticker)
    price = stock.info["currentPrice"]

    # Print check
    #print(ticker)
    #print(price)

    return price

# This function cycles through the companies table in our
# SQL database and returns all entries as a dictionary

def company_cycle():
    # Returns a dictionary of IDs and Tickers
    product_info = {}
    cursor.execute("SELECT company_id,ticker FROM companies")

    table = cursor.fetchall()

    # Print check
    #print("Company Cycle")

    for row in table:

        # Princt check
        #pprint(row)

        # Unpacking
        (cid, ticker) = row
        product_info.update({cid:ticker})

    return product_info

# This function loads stock prices into the SQL database

def load_stock():

    comp_dict = company_cycle()

    for c_id in comp_dict:

        # Print check
        #print(c_id)
        #print(comp_dict[c_id])

        cid = str(c_id)

        # Get the price for the current product
        price = get_stock_price(comp_dict[c_id])

        cursor.execute("SELECT price FROM stocks WHERE company_id = " + cid +" ORDER BY date desc LIMIT 1")
        stock_last_price = float(cursor.fetchall()[0][0])

        pct_change = str(round((price - stock_last_price) / stock_last_price,4))

        sprice = str(price)

        cursor.execute('''
                INSERT INTO stocks(date,price,company_id,pct_change)
                VALUES ( NOW(),'''+sprice+","+cid+","+pct_change+");")

    conn.commit()
    #print("Completed.")


# Run all the functions and load new prices to the database

monthday = ["01","08","16","23"]
t = date.today()
today =t.strftime("%d")

if today in monthday:
    # Run the load functions and add new data to tables
    load_price()
    load_stock()

else:
    pass
