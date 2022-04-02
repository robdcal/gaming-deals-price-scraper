import sys
import logging
import rds_config
import pymysql
import random, decimal, time, requests
from bs4 import BeautifulSoup
#rds settings
rds_host  = "rds-mysql-gaming-pricechecker.cxskvnnv0goh.eu-west-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    print ("1")
    connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    print ("2")
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    cursor = connection.cursor()
    print ("3")
    cursor.execute("SELECT * FROM Pages")
    print ("4")
    pages = cursor.fetchall()
    for page in pages:
        print(page)
        url = page[0]
        retailer = page[1]
        product_id = page[2]
        get_price = ''
        if retailer == "Argos":
            get_price = 'soup.find("div", itemprop="mainEntityOfPage").find("li", itemprop="price")["content"]'
        elif retailer == "GAME":
            get_price = 'soup.find("div", class_="buyingOptions").find("strong", class_="btnPrice").text'
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        price = eval(get_price)
        if price.startswith("£",0):
            price = price[1:]
        mySql_insert_query = """INSERT INTO Prices (url, price, product_id) VALUES (%s, %s, %s)"""
        cursor.execute(mySql_insert_query, (url, price, product_id))
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into table")
        time.sleep(1)
    cursor.close()