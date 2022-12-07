from time import sleep, perf_counter
from .models import Product
import urllib.request as req
import os
import requests
from random import randrange
from datetime import date, timedelta


class Tiki:
  category_list = {
    '49458': 'ao-khoac-gio',
    '49602': 'tui-xach-vua-va-nho',
    '49620': 'giay-the-thao-nam-co-thap',
    '8513': 'dong-ho-the-thao-nam',
    '8351': 'balo-nam',
    '29010': 'laptop-truyen-thong',
    '49512': 'ao-hoodies-nam-vai-ni',
    '49650': 'tui-bao-tu-tui-deo-bung',
    '8341': 'non-nam'
  }
  cookies = {
    '_trackity': 'c638e641-f74d-7230-982c-9b73edb27bcf',
    'G_ENABLED_IDPS': 'google',
    'amp_99d374_tiki.vn': 'o694UeL9ZWNF7QztlPNngK.MTAxODI1MTA=..1g4kvv5v6.1g4l26k4o.2i.3m.68',
    '_ym_d': '1658454922',
    '_ym_uid': '1658454922598576997',
    '_hjSessionUser_522327': 'eyJpZCI6IjU4YmFkOTliLTgyYWItNWVhZi05MGY4LTRmMDA5ODhjOTAyZSIsImNyZWF0ZWQiOjE2NTg0NTQ5MjA5NjUsImV4aXN0aW5nIjp0cnVlfQ==',
    '_gac_UA-15036050-1': '1.1658659624.Cj0KCQjw2_OWBhDqARIsAAUNTTEs54ewcml7tEOmM91Rey1gYL23xikr6uoviiZ7GdKMlUseUfF0XDQaAsGzEALw_wcB',
    '_gcl_aw': 'GCL.1658659624.Cj0KCQjw2_OWBhDqARIsAAUNTTEs54ewcml7tEOmM91Rey1gYL23xikr6uoviiZ7GdKMlUseUfF0XDQaAsGzEALw_wcB',
    '_gcl_au': '1.1.1932945221.1665141843',
    '__iid': '749',
    '__su': '0',
    '_bs': '53cc18d5-8f97-1cfe-843a-e0b458944654',
    'TKSESSID': '547b2308ab5956f766a6477157ed7b14',
    '_ga_43JLXF8LVL': 'GS1.1.1665238206.1.1.1665238230.0.0.0',
    'TOKENS': '{%22customer_id%22:10182510%2C%22access_token%22:%22eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMDE4MjUxMCIsImlhdCI6MTY2NjAwNDQ0MSwiZXhwIjoxNjY2MDkwODQxLCJpc3MiOiJodHRwczovL3Rpa2kudm4iLCJjdXN0b21lcl9pZCI6IjEwMTgyNTEwIiwiY2xpZW50X2lkIjoidGlraS1zc28iLCJzY29wZSI6InNzbyJ9.WvH68bAFpUUW9tY34Nu1VFF_lkkvrI5MkZcZirowCe6c-oESRBkP2ICGO6R2IRTCFgA1V8XWmqfm1u1uROExMLejwVmQ-fsKX9fNpxU4NIyw6EbDdPsYlNoC7z-T6ynn0LFhSuNSI5AOFIBF_ZL4EgZ1m1cTFFVQjok29Bb2K2w2ACnyFy9DgdVERkS0edX4ez1xfIIKXnM7MQaO8pmwpNHFk9R2Y8DZRVH6VfMpJaLDbx3H5lJyw_Z1WCaNSquHDs0SrSu1mhods8IG6VMJXIsJxfNdaSuOWu5SE0piSqrkIDN8iG8YsBaT09VcGh-THl8V2yTUnT61lZ4RMWw8WrP0gKkhrHLal9dpmBZmhbCRo8rwzR82LgGE0PJeQnLkXBH27PyOD2LbXwRGeAYpjeKWZJJxj_kzsXfOTfhLXax3xycf0Ga2foI2D0axs8x6SOU1TGxzXfMIZkwcOKZb8N4FInsWphPfevLtaNE74eQZiekk4xyMMVeh1WnALNjsHE52fntYzymeDpBKMg99_DPlJXqDS4AUE4JaK-8-DxN0NOCB-Iux--YWXzuoZtZl3AKDj1LiP4gJfyFu4B3N2dxcYnuNXB3g9IAt83FnFsIC-oaQLl2liXVhAGlRqilM3s7jD3cZw3NCQezSdIep49SQzleWdWFgTUbf2gansDs%22%2C%22token_type%22:%22bearer%22%2C%22refresh_token%22:%22TKIAgh9tb1HvDRNIcLyab8pjb5clzDPM_hNXAxNpfO9EefxKGEot_Q1vNHVhFR-el64z1y9Uh527G7CWhbEP%22%2C%22expires_in%22:86400%2C%22expires_at%22:1666090841484}',
    'TIKI_ACCESS_TOKEN': 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMDE4MjUxMCIsImlhdCI6MTY2NjAwNDQ0MSwiZXhwIjoxNjY2MDkwODQxLCJpc3MiOiJodHRwczovL3Rpa2kudm4iLCJjdXN0b21lcl9pZCI6IjEwMTgyNTEwIiwiY2xpZW50X2lkIjoidGlraS1zc28iLCJzY29wZSI6InNzbyJ9.WvH68bAFpUUW9tY34Nu1VFF_lkkvrI5MkZcZirowCe6c-oESRBkP2ICGO6R2IRTCFgA1V8XWmqfm1u1uROExMLejwVmQ-fsKX9fNpxU4NIyw6EbDdPsYlNoC7z-T6ynn0LFhSuNSI5AOFIBF_ZL4EgZ1m1cTFFVQjok29Bb2K2w2ACnyFy9DgdVERkS0edX4ez1xfIIKXnM7MQaO8pmwpNHFk9R2Y8DZRVH6VfMpJaLDbx3H5lJyw_Z1WCaNSquHDs0SrSu1mhods8IG6VMJXIsJxfNdaSuOWu5SE0piSqrkIDN8iG8YsBaT09VcGh-THl8V2yTUnT61lZ4RMWw8WrP0gKkhrHLal9dpmBZmhbCRo8rwzR82LgGE0PJeQnLkXBH27PyOD2LbXwRGeAYpjeKWZJJxj_kzsXfOTfhLXax3xycf0Ga2foI2D0axs8x6SOU1TGxzXfMIZkwcOKZb8N4FInsWphPfevLtaNE74eQZiekk4xyMMVeh1WnALNjsHE52fntYzymeDpBKMg99_DPlJXqDS4AUE4JaK-8-DxN0NOCB-Iux--YWXzuoZtZl3AKDj1LiP4gJfyFu4B3N2dxcYnuNXB3g9IAt83FnFsIC-oaQLl2liXVhAGlRqilM3s7jD3cZw3NCQezSdIep49SQzleWdWFgTUbf2gansDs',
    'TIKI_USER': 'BDqPGVwoWB9M58JIH53MpQgE48%2FBVHN9P0re6dyho4Sa5PkCoWdGiW1MyzPM8RgEGr0B9%2Fr%2BhmBy',
    'bnpl_whitelist_info': '{%22content%22:%22Mua%20tr%C6%B0%E1%BB%9Bc%20tr%E1%BA%A3%20sau%22%2C%22is_enabled%22:false%2C%22icon%22:%22https://salt.tikicdn.com/ts/tmp/f3/8d/17/c6d9012c6d8cc9681600561a8f620cf7.png%22%2C%22deep_link%22:%22https://tiki.vn/mua-truoc-tra-sau/dang-ky?src=account_page%22}',
    'delivery_zone': 'Vk4wMjYwMDcwMDQ=',
    '_gid': 'GA1.2.1303808069.1666004448',
    'tiki_client_id': '972293973.1654267027',
    '_hjSession_522327': 'eyJpZCI6IjY0NTU5MzU5LWI2MzctNDhjZi05NWEyLWY3MTRlOTAwNWYwMyIsImNyZWF0ZWQiOjE2NjYwMDQ0NTIwNjcsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '1',
    '_hjIncludedInPageviewSample': '1',
    '_hjIncludedInSessionSample': '0',
    '_gat': '1',
    'amp_99d374': 'o694UeL9ZWNF7QztlPNngK.MTAxODI1MTA=..1gfipkskd.1gfiu2m6e.bk.et.qh',
    '_ga': 'GA1.1.972293973.1654267027',
    'cto_bundle': 'ht_vAV9XbGRmVDk1MDhQR01ab2FNY2djWkt3RHpyT1VkNWF6WEQ3VkxDYVh0RjIyZXpZeEd4RGxaR2NWTURFeHNtRThXT0dYOTlLU0dVcUZ5VU5VaTM2aEd0eUtTSm1XbTdsU0tOWTZWeldIOE1xakl5RFlJUU5hWDBHUXJ1YmhlZEtuVg',
    '_gali': '__next',
    '_ga_GSD4ETCY1D': 'GS1.1.1666004451.13.1.1666009114.35.0.0'
  }

  def crawl(self):
    count = 1
    for key, value in self.category_list.items():
      headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://tiki.vn/' + value + '/c' + key,
        'x-access-token': 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMDE4MjUxMCIsImlhdCI6MTY2NjAwNDQ0MSwiZXhwIjoxNjY2MDkwODQxLCJpc3MiOiJodHRwczovL3Rpa2kudm4iLCJjdXN0b21lcl9pZCI6IjEwMTgyNTEwIiwiY2xpZW50X2lkIjoidGlraS1zc28iLCJzY29wZSI6InNzbyJ9.WvH68bAFpUUW9tY34Nu1VFF_lkkvrI5MkZcZirowCe6c-oESRBkP2ICGO6R2IRTCFgA1V8XWmqfm1u1uROExMLejwVmQ-fsKX9fNpxU4NIyw6EbDdPsYlNoC7z-T6ynn0LFhSuNSI5AOFIBF_ZL4EgZ1m1cTFFVQjok29Bb2K2w2ACnyFy9DgdVERkS0edX4ez1xfIIKXnM7MQaO8pmwpNHFk9R2Y8DZRVH6VfMpJaLDbx3H5lJyw_Z1WCaNSquHDs0SrSu1mhods8IG6VMJXIsJxfNdaSuOWu5SE0piSqrkIDN8iG8YsBaT09VcGh-THl8V2yTUnT61lZ4RMWw8WrP0gKkhrHLal9dpmBZmhbCRo8rwzR82LgGE0PJeQnLkXBH27PyOD2LbXwRGeAYpjeKWZJJxj_kzsXfOTfhLXax3xycf0Ga2foI2D0axs8x6SOU1TGxzXfMIZkwcOKZb8N4FInsWphPfevLtaNE74eQZiekk4xyMMVeh1WnALNjsHE52fntYzymeDpBKMg99_DPlJXqDS4AUE4JaK-8-DxN0NOCB-Iux--YWXzuoZtZl3AKDj1LiP4gJfyFu4B3N2dxcYnuNXB3g9IAt83FnFsIC-oaQLl2liXVhAGlRqilM3s7jD3cZw3NCQezSdIep49SQzleWdWFgTUbf2gansDs',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
      }
      params = {
        'limit': '40',
        'include': 'advertisement',
        'aggregations': '2',
        'trackity_id': 'c638e641-f74d-7230-982c-9b73edb27bcf',
        'category': key,
        'page': '1',
        'urlKey': value
      }
      new_dir = os.path.join('./static/images_data/tiki/', 'tk_category_' + str(count))
      if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

      for i in range(1, 50):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)
        if response.status_code == 200:
          print('request success')
          if response.json().get('data') is None:
            break
          if i == 1:
            with open('./static/crawl/tiki/log/' + str(date.today() + timedelta(days=1)) + "_" + key + ".log",
                      "a+") as file:
              file.write(f"{response.json().get('data')[0]['id']}\n")
          for record in response.json().get('data'):
            exists = False
            product_id = str(record.get('id'))
            with open('./static/crawl/tiki/log/' + str(date.today()) + "_" + key + ".log", "a+") as file:
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
            ctime = '1668490991'
            name = record.get('name')
            price = str(record.get('price'))
            image = record.get('thumbnail_url')
            link = 'https://tiki.vn/' + record.get('url_path')
            rating = quantity_sold = discount = 0
            if record.get('rating_average'):
              rating = str(record.get('rating_average'))
            if record.get('quantity_sold'):
              quantity_sold = str(record.get('quantity_sold')['value'])
            if record.get('original_price') > 0:
              discount = str(100 - int(record.get('price') / record.get('original_price') * 100))
            img_data = requests.get(image).content
            with open('./static/images_data/tiki/tk_category_' + str(count) + '/tk_' + str(record.get('id')) + '.jpg',
                      'wb') as handler:
              handler.write(img_data)
            file = open('./static/crawl/tiki/sql/' + str(date.today() + timedelta(days=1)) + "_" + key + ".sql", "a+",
                        encoding='utf-8')
            file.write(
              "INSERT INTO products VALUES(null," + f"'tk_{product_id}'" + ", " + f"\"{name}\"" + ", " + f"'{price}'" + ", " + f"'{link}'" + ", " + f"'{image}'" + ", " + f"{ctime}" + ", 'Tiki'" + ", " + f"{discount}" + ", " + f"{quantity_sold}" + ", " + f"{rating}" + ");\n")
            file.close()
        sleep(randrange(3, 11))
      count = count + 1
