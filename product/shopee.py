import os

import requests
from time import sleep
from datetime import date, timedelta

class Shopee:
  category_list = {
    '11035572': 'ao-vest',

  }
  headers = {
    'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhE+zZswAAAtYAj4AAAAAAAAAAOYyhFAbVQMMpIKa2+dGIBkKaWUVkWOzjLDykZY2dhCO2aemlrO8uBg4H76sb4kvBSiAzpqfJ4b+sa91AUY0aUmD179fHlmolDe2PGWvmQcgUD/RMvb920nsmCzc3MjyCUzFHboPIj3kY5Bsh5Nwc9E1wb6Kwx+sHYUksk1c7UwQToOSxQRnTxM7z8+yW9TjxmhsoclUrLni5ioX/ooVKxEmyKW3UW+QQ6pjMKk4isCGWw9ufZRIxMPWHatc3DJxrLbxnaL+fxXNIy7mvkK63w3LxpgTWyrFKlyeg2pnxy4dU+D+JXOHVeeJNvqYso4XqTBJlvEjgWfNNLiT5e1wPvI/KL073xtxDWHC58kjywRwzXXhW1Fx4u2YAcw9BtP2J3gkf9mFirCBwj5OCqLM+pe9xRdl/jf0909IHtxuTs1+zBMZrQEmSA138OeJlMLraFMKanP+fxXNIy7mvkK63w3LxpgTDH7N7Gvy4QYqtzTZMFP6rewlSoQqAjuvVdaec1j4FR3s5/YTy8Z7G8POxRxaE7hTmmlMQ+JYTMHF6kF68iRD863AXn4GZq4rQBRGB/GvgD2PtAjZpkh/j/IObl8KuExVBenj5gvv11oO9Stg2MAUZRC3q7r7Amu/FcS/fiwQIrKIho5LxORIkIvYHmXWjcsYEz9S9S9p+tV1HIfZaPBju4tseKGzPm/cik0cHJIHLjqRY7OMsPKRljZ2EI7Zp6aWkWOzjLDykZY2dhCO2aemlnd2VeCw3RUtmnRJCucetbY=',
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
    'view_session_id': 'f6a1309f-87ab-429a-9455-3cb6e0429dfd'
  }

  def crawl(self):
    dircount = 1
    count = 0
    for category in self.category_list:
      new_dir = os.path.join('./static/images_data/shopee/', 'sp_category_' + str(dircount))
      if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
      for i in range(0, 25):
        count = count + 1
        if self.params['newest'] == 0:
          self.params['newest'] = self.params['newest'] + 60 * i
        else:
          self.params['newest'] = 60 * i
        response = requests.get(
          'https://shopee.vn/api/v4/search/search_items',
          headers=self.headers,
          params=self.params
        )
        if response.json().get('items') == None:
          print('request blocked!')
          count = 0
          break
        if i == 0:
          with open('./static/crawl/shopee/log/'+str(date.today() + timedelta(days=1)) + "_" + self.params['match_id'] + ".log", "a+") as file:
            file.write(f"{response.json().get('items')[0]['itemid']}\n")
        for record in response.json().get('items'):
          exists = False
          product_id = str(record.get('item_basic')['itemid'])
          with open('./static/crawl/shopee/log/'+str(date.today()) + "_" + self.params['match_id'] + ".log", "a+") as file:
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
          name = record.get('item_basic')['name']
          price = str(record.get('item_basic')['price'])
          image = "https://cf.shopee.vn/file/" + str(record.get('item_basic')['image'])
          link = "https://shopee.vn/" + record.get('item_basic')['name'] + '-i.' + str(
            record.get('shopid')) + '.' + str(record.get('item_basic')['itemid'])
          img_data = requests.get(image).content
          with open('./static/images_data/shopee/sp_category_' + str(dircount) + '/sp_' + product_id + '.jpg',
                    'wb') as handler:
            handler.write(img_data)
          file = open('./static/crawl/shopee/sql/'+str(date.today() + timedelta(days=1)) + "_" + self.params['match_id'] + ".sql", "a+", encoding='utf-8')
          file.write(
            "INSERT INTO products VALUES(null," + f"'sp_{product_id}'" + ", " + f"\"{name}\"" + ", " + f"'{price[:len(price) - 5]}'" + ", " + f"'{link}'" + ", " + f"'{image}'" + ", " + f"{ctime}" + ", 'Shopee'"+");\n")
          file.close()
        if count == 10:
          count = 0
          dircount += 1
          sleep(60 * 30)

