# Realtor Web Scrapping
## Setting Up
```bash
conda activate PIC16B-24F
scrapy startproject Property_scraper
cd Property_scraper
```
## Experiments
```bash
scrapy shell https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA
```
The following CSS selector that works:
```bash
response.css('div[id^="property_id_"] a::attr(href)').getall()
```
I documented this in the "property_spider.py"
The following CSS selector that meant to press the next buttom does not work,
I tried the following:
```bash
response.css('a.next-link::attr(href)').get()
response.css('div[aria-label="pagination"] a[rel="next"]::attr(href)').get()
response.css('div[aria-label="pagination"] a.next-link::attr(href)').get()
response.xpath('//div[@aria-label="pagination"]//a[contains(@class, "next-link")]/@href').get()
```
I gave up in follow the "Next" buttom, so I just manually build the url on spider.

## To Scrape Links on Property Page
After changing directory to Property_scraper, type the following on the terminal window to download links to each property and save the results as "results.csv". This will give you the links to each property listed on page one of https://www.realtor.com/realestateandhomes-search/90024.  
```bash
scrapy crawl property_spider -o results.csv
```
Note that the parse() method only extracted 8 urls from this page. There are more listings on the first page that should've been extracted. This may be due to how realtor.com displays listings dynamically using JavaScript, which prevents us from scraping all listings from the initial HTML source. To fix this issue, we may need to use tools such as Selenium or Splash from Scrapy. 
