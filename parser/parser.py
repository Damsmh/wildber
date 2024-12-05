from curl_cffi import requests

class Parser:
        
    def format_query_items(self, products_raw):
        products = []
        products.append({'count': 20})
        if products_raw != None and len(products_raw) > 0:
            for product in products_raw:
                if len(products) == 20:
                    break
                id = product.get('id', None)
                vol = id // 100_000
                host = self.get_host(vol) 
                products.append({'id': id,
                                 'preview': f'https://basket-{host}.wbbasket.ru/vol{vol}/part{id // 1_000}/{id}/images/big/1.webp',
                                 'name': product.get('name', None), 
                                 'brand': product.get('brand', None),
                                 'reviewRating': product.get('reviewRating', None),
                                 'feedbacks': product.get('feedbacks', None),
                                 'link': f'https://www.wildberries.ru/catalog/{id}/detail.aspx',
                                 'price': int(product.get('sizes', None)[0].get('price', None).get('product'))/100,
                })
        return products
    
    def format_article_item(self, product_raw):
        types = None
        if product_raw != None:
            types = []
            if len(product_raw) > 0:
                for product in product_raw:
                    id = product.get('id', None)
                    vol = id // 100_000
                    host = self.get_host(vol) 
                    try:
                        price = int(product.get('sizes', None)[0].get('price', None).get('product'))/100
                    except:
                        price = 0
                    types.append({'id': id,
                                  'preview': f'https://basket-{host}.wbbasket.ru/vol{vol}/part{id // 1_000}/{id}/images/big/1.webp',
                                  'name': product.get('name', None), 
                                  'brand': product.get('brand', None),
                                  'reviewRating': product.get('reviewRating', None),
                                  'feedbacks': product.get('feedbacks', None),
                                  'link': f'https://www.wildberries.ru/catalog/{id}/detail.aspx',
                                  'price': price,
                    })
        return types
    
    def get_host(self, vol: int):
        host = ''
        if vol >= 0 and vol <= 143: host = '01'
        elif vol >= 144 and vol <= 287: host = '02'
        elif vol >= 288 and vol <= 431: host = '03'
        elif vol >= 432 and vol <= 719: host = '04'
        elif vol >= 720 and vol <= 1007: host = '05'
        elif vol >= 1008 and vol <= 1061: host = '06'
        elif vol >= 1062 and vol <= 1115: host = '07'
        elif vol >= 1116 and vol <= 1169: host = '08'
        elif vol >= 1170 and vol <= 1313: host = '09'
        elif vol >= 1314 and vol <= 1601: host = '10'
        elif vol >= 1602 and vol <= 1655: host = '11'
        elif vol >= 1656 and vol <= 1919: host = '12'
        elif vol >= 1920 and vol <= 2045: host = '13'
        elif vol >= 1920 and vol <= 2189: host = '14'
        elif vol >= 1920 and vol <= 2405: host = '15'
        elif vol >= 1920 and vol <= 2621: host = '16'
        elif vol >= 1920 and vol <= 2837: host = '17'
        else: host = '18'
        return host
    
    def get_product_types(self, article: int):
        id = article
        vol = id // 100_000
        host = self.get_host(vol)
        url_colors = f'https://basket-{host}.wbbasket.ru/vol{vol}/part{id // 1_000}/{id}/info/ru/card.json'
        colors = requests.get(url_colors, impersonate='chrome').json().get('colors', None)
        url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&ab_testing=false&nm={';'.join(map(str, colors))}"
        response = requests.get(url, impersonate="chrome").json()
        product_raw = response.get('data', {}).get('products', None)
        return product_raw
            
    def get_search_products(self, query: str):
        url = f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-1255987&query={'%20'.join(query.split())}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        response = requests.get(url, impersonate="chrome").json()
        products_raw = response.get('data', {}).get('products', None)
        return products_raw

    def get_article_product(self, article: str):
        url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&ab_testing=false&nm={article}"
        response = requests.get(url, impersonate="chrome").json()
        product_raw = response.get('data', {}).get('products', None)
        return product_raw
    
    def search_query(self, query):
        response = self.get_search_products(query)
        return self.format_query_items(response)
    def search_product_types(self, article):
        response = self.get_product_types(article)
        return self.format_article_item(response)
    def search_article(self, article):
        response = self.get_article_product(article)
        return self.format_article_item(response)
        

