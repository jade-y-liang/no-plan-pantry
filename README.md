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
The following CSS selector does not fully function, but it do returns a list of link to follow:
```bash
response.css('div[id^="property_id_"] a::attr(href)').getall()
```
I documented this in the "property_spider.py"

