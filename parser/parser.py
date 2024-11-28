from curl_cffi import requests

class Parser:
    def __init__(self):
        self.headers = {'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',}
        
    def format_items(self, products_raw):
        
        products = []
        
        if products_raw != None and len(products_raw) > 0:
            for product in products_raw:
                id = product.get('id', None)
                products.append({'id': id, 
                                 'preview': f'https://basket-10.wbbasket.ru/vol{str(id)[:4]}/part{str(id)[:6]}/{str(id)}/images/big/1.webp',
                                 'name': product.get('name', None), 
                                 'brand': product.get('brand', None),
                                 'reviewRating': product.get('reviewRating', None),
                                 'feedbacks': product.get('feedbacks', None),
                                 'link': f"https://www.wildberries.ru/catalog/{id}/detail.aspx",
                                 'price': int(product.get('sizes', None)[0].get('price', None).get('product'))/100})
        return products
            
    def get_search_products(self, query: str):
        url = f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-1255987&query={'%20'.join(query.split())}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        response = requests.get(url, impersonate="chrome").json()
        products_raw = response.get('data', {}).get('products', None)
        return products_raw
    
    def add_db():
        pass
    
    def run(self, query):
        response = self.get_search_products(query)
        return self.format_items(response)
        
parser = Parser()
