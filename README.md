# Stock Product Comparator
Comparator tracking stock price and keystone product prices for select companies

# How it works
The stock product comparator automatically pulls stock price data for Proctor & Gamble, The Vita Coco Company, and Kimberly-Clark and tracks changes against keystone products for each company, namely Tide Pods, Coconut Water, and Kleenex.

My Python scraper script, saved here as scraper.py, runs daily on PythonAnywhere and saves new data to a SQL database on Bit.io. CSV files here in GitHub are updated regularly, and feed into visualizations created with Datawrapper.

# What is this for?
In 2022, fabric and home care products, including the juggernaut Tide brand, generated 31% of net earnings for consumer goods conglomerate P&G. Similarly, organic coconut water is the lifeblood of the smaller Vita Coco Company. 

Though exogenous factors including macroeconomic shifts and sentiment among institutional investors frequently impact share prices for publicly-traded companies, how companies price their products, especially keystone products like Tide with an outsized impact on revenue, sits at the root of profitability, growth, and competitiveness. 

You won’t find correlation metrics between product prices and share prices on Yahoo Finance or the dashboard of your broker of choice, though, and for good reason. Gross margin is cleaner, and crucially there is no single source of truth for the price of a given product. Further, stock prices aren’t impacted just a company’s fundamentals, but by float and general sentiment, too. 

Product pricing, however, has the potential to be a leading indicator for a company’s performance. This experiment explores this hypothesis, tracking the relationship between product prices and share prices over time.

# Discussion & Results
See my post for results: https://tyssweeney.com/pricing/
