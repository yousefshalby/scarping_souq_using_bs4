from bs4 import BeautifulSoup
import requests
import json
import time
import csv, os
from urllib.request import unquote

class iphone:
    base_url =  'https://egypt.souq.com/eg-en/iphone-12-pro/s/?as=1&section=1&page='

    def fetch(self, url):
        print ('http get request: %s ' %url, end = '')
        res = requests.get(url)
        print(' | Status code: %s' % res.status_code)    
    
        return res

    def parse(self, html):
        content = BeautifulSoup(html,'lxml')
        title = [titles.text.replace("\n\t\t\t\t", '').replace("\n\t\t\t", "") for titles in content.find_all('h1', {'class':'itemTitle'})]
        all_urls =[items['href'] for items in content.find_all('a',{'class':'view-product-details sPrimaryLink secondary button expand white tiny'})]
        images = [img['data-src'] for img in content.find_all('img', {'class':'img-size-medium imageUrl'})]
        prices = [price.text for price in content.find_all('h3', {'class':'itemPrice'})]
        descriptions = [description.text.replace("\n","") for description in content.find_all('ul', {'class':'selling-points'})]

        for index in range(0, len(title)):
            items = {
                'title': title[index], 
                'image': images[index],
                'prices': prices[index],
                'descriptions': descriptions[index],
                'urls': all_urls[index],
                }

            print(json.dumps(items, indent=2))
            for image in images:
                self.download_images(image)
                time.sleep(2)
            
    def download_images(self, image):        
            response = requests.get(image)
            file_name = unquote(response.url).split('item_L_13')[-1]
            with open ('.\images\\' + file_name, "wb") as image_file:
                for chunk in response.iter_content(chunk_size = 128):
                    image_file.write(chunk)

    def run(self):
        headers = {
            "accept-encoding":" gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "referer":" https://egypt.souq.com/eg-en/iphone-12-pro/s/?as=0&section=2&page=1",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site":" same-origin",
            "user-agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        }

        params={
            "as":0,
            "section":1,
        }

        for page in range(1,3):
            next_page = self.base_url + str(page)
            print (next_page)
            res=self.fetch(next_page)
            if res.status_code ==200:
                self.parse(res.text)
                params['section'] +=1
                time.sleep(3)
            else:
                print ('somthing went wrong')      
                continue

if __name__ == '__main__':
    scraper = iphone()
    scraper.run()                
