# Realtor Web Scraping
## Setting Up
```bash
conda activate PIC16B-24F
scrapy startproject Recipe_scraper
cd Recipe_scraper
```
## Output Data
```bash
scrapy crawl recipe_spider -o results.csv 
```

## To Scrape Links on Property Page
After changing directory to Property_scraper, type the following on the terminal window to download links to each property and save the results as "results.csv". This will give you the links to each property listed on page one of https://www.realtor.com/realestateandhomes-search/90024.  
```bash
scrapy crawl property_spider -o results.csv
```
Note that the parse() method only extracted 8 urls from this page. There are more listings on the first page that should've been extracted. This may be due to how realtor.com displays listings dynamically using JavaScript, which prevents us from scraping all listings from the initial HTML source. To fix this issue, we may need to use tools such as Selenium or Splash from Scrapy. 
