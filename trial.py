from bs4 import BeautifulSoup
import requests
import time

names=[]
prices=[]

#/search/searchresults.aspx?type=product&filter=brandName%3aSAMSUNG%3bcategory%3aTV & Home Theatre&fromBrandStore=samsung&lang=en&page=2
#/Search/SearchResults.aspx?type=product&filter=brandName%253aSAMSUNG%253bcategory%253aTV%20%26%20Home%20Theatre&fromBrandStore=samsung&page=2

url = "https://www.bestbuy.ca/en-CA/Search/SearchResults.aspx?type=product&filter=brandName%253aSAMSUNG%253bcategory%253aTV%20%26%20Home%20Theatre&fromBrandStore=samsung"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page=1
while True:
    r = requests.get(url, headers=headers)
    html_doc = r.content
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    
    elements = soup.findAll('h4', attrs={'class': 'prod-title'})
    for el in elements:
        names.append(el.text.strip("\n"))
    
    elements_2 = soup.findAll('span', attrs={'class':'amount'})
    for el in elements_2:
        prices.append(el.text)
    
    pages = []
    elements_3 = soup.findAll('ul', attrs={'class':"pagination-control inline-list"})
    for el in elements_3:
        children = el.findChildren("li" , recursive=False)
        for child in children:
            children_2 = child.findChildren("a" , recursive=False)
            for child in children_2:
                pages.append(child['data-page'])
    max_page=int(max(pages))+1
    print("Page: ",page)
    page+=1
    url = "https://www.bestbuy.ca/en-CA/Search/SearchResults.aspx?type=product&filter=brandName%253aSAMSUNG%253bcategory%253aTV%20%26%20Home%20Theatre&fromBrandStore=samsung&page="+str(page)
    time.sleep(2) 
    
    if page==max_page:
        break
    

import pandas as pd
df = pd.DataFrame(
    {'name': names,
     'price': prices
    })
    
df.to_csv('file.csv', sep=',', encoding='utf-8')
