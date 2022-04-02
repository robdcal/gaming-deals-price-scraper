# Gaming Deals Price Scraper

I created this project around October 2020, just before the PlayStation 5 was launching. It was designed to scrape the prices of consoles, games and accessories from multiple online retailers and display them to users on a retail-like price comparison website.

This repository holds just a single file that I hope helps to demonstrate the idea, however the full project was much bigger and involved AWS cloud services and a WordPress website.

## The Setup

- Python scripts for scraping the data using BeautifulSoup (also tried using Pytesseract for those pesky ShopTo prices that are baked into an image!!) and storing the results
- An EC2 server to run the python scripts
- Lambda / EventBridge to schedule the spinning up and winding down of the EC2 server to reduce costs
- An RDS MySQL database with several tables to store all of the data needed for the scraper, and storing all of the scraped data itself
- A WordPress website with product categories that tapped into the RDS database for the pricing data
- Chart.js for display some of the data in a chart (showing price history over time)
