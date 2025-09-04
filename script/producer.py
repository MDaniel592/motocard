import ujson
import time
from curl_cffi import requests
from lxml import html
from datetime import datetime
from nats.aio.client import Client as NATS
import asyncio

class Motocard():

  def init(self):
    self.name = 'Motocard'
    self.base_url = 'https://www.motocard.com'
    self.headers  = {
      "Host": "www.motocard.com",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
      "Accept": "application/json, text/javascript, */*; q=0.01",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate, br",
      "Cookie": "mtc_different_country_accepted=eyJpdiI6IjRuYndHSmVUZW9oTEdWSlZmaEhaRkE9PSIsInZhbHVlIjoiOVUzS2JLNXNualpaam4rRmcvM3Z0dz09IiwibWFjIjoiN2ZkMzlhZDMzNDA0Nzk3YWQ3NDE5Y2U0NzFkODkxNTY5YTgyZDZlZTE2ZTlkNTk5ZTUyNGQ1ZjQ2ZjIxZGYxYSIsInRhZyI6IiJ9; MTC-XSRF-TOKEN=eyJpdiI6IjB6Y3g2dXZJNFVzSi9YM3BSUW5mS2c9PSIsInZhbHVlIjoidStaTXNsb0FpRm01Si9zYnRPbFExU0tpQTJlV1JLN0JEbFRETkN1dm1EZHY1anNXZzVFT05oa01OMFZzT1hLQ1p0T0FNTzAycDBZN29QSjJGR0hYV3c9PSIsIm1hYyI6IjYwY2U0ZThkM2M4YjU3YzA2MTU1OTY4NjE3ZmRhZDFmZTVlZWExZTkzMDMzN2Y4N2QwYTRkNmNiZmZmMTFkNDYiLCJ0YWciOiIifQ%3D%3D; shared_laravel_session=eyJpdiI6Ik1xbzZ1T1FYQmRBRTlXaG54aTNJK3c9PSIsInZhbHVlIjoiRDl0MHhVMHlNaFdrYTJsVWdPRzUvd2RVYzJ6KzZtczJoOTlKRnI1dlZDTDVzeUpIbmYzZmhJZk9BTEdoWUJwbHBhck9QOStyUWExNTlmTzZGZ2ZqL0E9PSIsIm1hYyI6IjRkMjQ1OTk5Yjg1MjdhYzdhYWRjYWYxZTVlZGVkNGI0NDllMTJkNDZjMGE2ODc4N2RiMDdmZmM0ODgxNjQ5MDQiLCJ0YWciOiIifQ%3D%3D; mtc_user_sc=eyJpdiI6IlFGWWlyQ0lrdHVORXViWDFkak15SUE9PSIsInZhbHVlIjoiUVFVSU5VbHlwSWhNQm1HRGtpL0s3Zz09IiwibWFjIjoiZDU3MTU0MmFmOTIyMzM1NTNlYzkzYzIzYjRmZWRmMWMyZWU4ZDk3MGMyZjU5NjQyZWUxNzM1MzZkY2RhNTBmYiIsInRhZyI6IiJ9; cf_clearance=y3CbO7x7QMSnynSwkBn.FeqzU54as7IBiVuQ8h6Tu1M-1751657257-1.2.1.1-2BuAxFUDHYGPkj_ZfrdDZs8K7CyKOS5VmLTzhSfIvMWec9hy252rLP4gxTT3OV2LAJiMRNKjfln3_FvH6jgoBb0MOi2JtZLijglOmNme0rIrwDHcQziGbtJHTT6Oj7VzvY3huN.JEFZy3r3JptwI3nAEAa7__XRSwouViwZCIXeCqq72B37Y8V3rG02mQRXpboCYpxBmzTrXmjbuSNE5zir2Jx9fqlOzCwQzBy.hMRU",
      "X-Requested-With": "XMLHttpRequest",
      "DNT": "1",
      "Connection": "keep_alive",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Sec-GPC": "1",
      "TE": "trailers",
    }


  async def get_product_stock(self, url, max_price):
    """
    Get the stock of a product from Motocard.
    """
    # Make a request to the product page
    response = requests.get(url, impersonate="chrome110", headers=self.headers)
    
    # Check if the request was successful
    if not response.status_code == 200:
      print(f"Request status code: {response.status_code}")
      return 'Product not found'	

    # Parse the response
    lxml_parser = html.fromstring(response.content)

    # Get product info from JSON  <script type="application/ld+json">
    json_data = lxml_parser.xpath('//script[@type="application/ld+json"]')
    if json_data:
      json_data = ujson.loads(json_data[0].text)
    else:
      return 'Product not found'

    # Check if the product is in stock
    stock = False
    availability = json_data.get('offers', {}).get('availability')
    if availability == 'http://schema.org/InStock' or availability == 'https://schema.org/InStock':
      stock = True      
    
    # Retrieve price
    price = json_data.get('offers', {}).get('price')

    # Retrieve product name
    product_name = json_data.get('name')

    # Retrieve sku
    sku = json_data.get('sku')

    if price >= max_price:
      print(f"Price too high {product_name} | Price: {price} | Stock: {stock} | SKU: {sku}")
      return 'Price too high'
  
    if stock == False:
      print(f"Out of stock {product_name} | Price: {price} | Stock: {stock} | SKU: {sku}")
      return 'Out of stock'
  
    # Connect to NATS server
    nc = NATS()
    await nc.connect("nats://nats:4222")

    # Mensaje a publicar
    msg = {
        'url': url,
        'product_name': product_name,
        'price': price,
        'stock': stock,
        'updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      }
    await nc.publish("tasks", ujson.dumps(msg).encode())

    print(" [x] Mensaje enviado a NATS")
    await nc.drain()

    
    return 'Stock information found'



motocard = Motocard()
motocard.init()
while True:
  products = [
    ('https://www.motocard.com/guantes/five-rfx1_v2_black_gf5rfx119108.aspx', 150),
    ('https://www.motocard.com/cascos/shoei-x_spr_pro_black.aspx', 600)
  ]
  for product in products:
    url, max_price = product
    asyncio.run(motocard.get_product_stock(url, max_price))
  
  
  time.sleep(300) # Sleep for 5 minutes
