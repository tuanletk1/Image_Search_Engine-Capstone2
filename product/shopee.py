import os

import requests
from time import sleep
from datetime import date, timedelta
from product.models import Product


class Shopee:
  category_list = {
    '11035572': 'ao-vest',
    '11035771': 'tui-quai-sach',
    '11035807': 'giay-sneaker',
    '11035789': 'dong-ho-nam',
    '11035742': 'balo',
    '11036015': 'laptop',
    '11035579': 'ao-hoodie',
    '11035752': 'tui-cheo',
    '11036402': 'mu'
  }
  headers = {
    'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhFAYYjgAAAsdAj8AAAAAAAAAAOYyhFAbVQMMpIKa2+dGIBkKaWUVkWOzjLDykZY2dhCO2aemlsl0+3Mvscq6m4kYsCCYCbK8HZ2GTC6Gy8upKta1Aomldqc0SLbNX/Vd0To2ioCeSir1BxMyVJSICSYiQU3orkmu45qllm6+jG+7VLZzEP8yEawhiuYAC9nnTHpeS5vAAfDkI0mSba/CXraQajo5fdS18ylDmIpexxyWlfUaRjfn5DtSUG9QIVLUSI3R8+2Vi2PuKPcEYrUGmGxYLfgyiKAYfR0WvgE2pJEUSvIqWlCgQTcGSDZJiUzeVA+6ZRBGqBTtUWs0KTvzqc2jwARQnFD7GGl7byJLfOsS3Gueo4KKBXI0QP+uzkK23PGHcOZztHAa4a+ojyWyvwAVCVkhTUxcJqaQNDvlDA7IiJvpFsgpeHQXx+lEECXlHknmoTTyjyH2kcATOJRGeOOLqHfQnnDX9TLS/Vg6VVpCXz4dPQEO9mqQPvi3woXAJNjl7BrG6/Se0PXcuF0t010rB/t3m2zxTEG07IlXOk89iH4UC8m+dS1Pa4pU6+Mj1UKNdCNC+vYB4rWCd+/ip6LSB4AyriTm2XJqZBCdVrNk6S4Qybs9Rj1CFl5xNyTigohzht/qk5ppTEPiWEzBxepBevIkQ/M9trFi4uTKRTjSpMkviDbkYH8s5mzdyRJB7iNTrYZnGWcoRy9iK4kRq5JnBseOinKRY7OMsPKRljZ2EI7Zp6aWkWOzjLDykZY2dhCO2aemliVII1tD7/IHSYGoATqdYXg=',
  }
  params = {
    'by': 'ctime',
    'limit': 60,
    'match_id': '11035572',
    'newest': 0,
    'order': 'desc',
    'page_type': 'search',
    'scenario': 'PAGE_CATEGORY',
    'version': 2,
    'view_session_id': '49da400e-9c6e-43ee-895c-58c07c3154d1'
  }

  def get_images(self):
    products = Product.objects.filter(shop='Shopee')
    count = 1
    dircount = 1
    for product in products:
      img_data = requests.get(product.images_link).content
      with open('./static/images_data/shopee/sp_category_' + str(dircount) + '/sp_' + product.original_id.replace('sp_',
                                                                                                                  '') + '.jpg',
                'wb') as handler:
        handler.write(img_data)
        count += 1
      if count == 1200:
        count = 0
        dircount += 1

  def crawl(self):
    dircount = 1
    count = 0
    for key, category in self.category_list.items():
      new_dir = os.path.join('./static/images_data/shopee/', 'sp_category_' + str(dircount))
      if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
      for i in range(0, 25):
        count = count + 1
        if self.params['newest'] == 0:
          self.params['newest'] = self.params['newest'] + 60 * i
        else:
          self.params['newest'] = 60 * i
        self.params['match_id'] = key
        while True:
          response = requests.get(
            'https://shopee.vn/api/v4/search/search_items',
            headers=self.headers,
            params=self.params
          )
          if response.json().get('items') == None:
            print('request blocked!')
            sleep(60 * 50)
            continue
          break
        if i == 0:
          with open('./static/crawl/shopee/log/' + str(date.today() + timedelta(days=1)) + "_" + self.params[
            'match_id'] + ".log", "a+") as file:
            file.write(f"{response.json().get('items')[0]['itemid']}\n")
        for record in response.json().get('items'):
          exists = False
          product_id = str(record.get('item_basic')['itemid'])
          with open('./static/crawl/shopee/log/' + str(date.today()) + "_" + self.params['match_id'] + ".log",
                    "a+") as file:
            file.seek(0)
            for line in file.readlines():
              if line.strip("\n") == product_id:
                print('ID already exists!')
                exists = True
                break
            else:
              file.write(f"{product_id}\n")
          if exists:
            continue
          ctime = str(record.get('item_basic')['ctime'])
          name = record.get('item_basic')['name'].replace('"', '\\"')
          price = str(record.get('item_basic')['price'])
          image = "https://cf.shopee.vn/file/" + str(record.get('item_basic')['image'])
          link = "https://shopee.vn/" + record.get('item_basic')['name'] + '-i.' + str(
            record.get('shopid')) + '.' + str(record.get('item_basic')['itemid'])
          rating = 0
          quantity_sold = 0
          discount = 0
          if record.get('item_basic')['item_rating']:
            rating = str(record.get('item_basic')['item_rating']['rating_star'])
          if record.get('item_basic')['sold']:
            quantity_sold = str(record.get('item_basic')['sold'])
          if record.get('item_basic')['raw_discount']:
            discount = str(record.get('item_basic')['raw_discount'])
          img_data = requests.get(image).content
          with open('./static/images_data/shopee/sp_category_' + str(dircount) + '/sp_' + product_id + '.jpg',
                    'wb') as handler:
            handler.write(img_data)
          file = open('./static/crawl/shopee/sql/' + str(date.today() + timedelta(days=1)) + "_" + self.params[
            'match_id'] + ".sql", "a+", encoding='utf-8')
          file.write(
            "INSERT INTO products VALUES(null," + f"'sp_{product_id}'" + ", " + f"\"{name}\"" + ", " + f"'{price[:len(price) - 5]}'" + ", " + f"'{link}'" + ", " + f"'{image}'" + ", " + f"{ctime}" + ", 'Shopee'" + ", " + f"{discount}" + ", " + f"{quantity_sold}" + ", " + f"{rating}" + ");\n"
          )
          file.close()
        if count == 10:
          count = 0
          dircount += 1
          sleep(60 * 50)
