# Redfin Housing Data Analysis

## Setting Up
* Here is the [link](https://www.unitedstateszipcodes.org/zip-code-database/#) to directly access a csv file containing all U.S. zip codes.
  * We used the free version. The csv file we used is also available in this repository. 
* [Python wrapper](https://github.com/reteps/redfin) created by another user to access data on a Redfin listing without screen scraping. 

<<<<<<< HEAD
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


