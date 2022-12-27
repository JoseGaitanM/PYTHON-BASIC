"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

import requests
import re 
from bs4 import BeautifulSoup

BASE_URL = "https://finance.yahoo.com/"
HEADERS = {'User-Agent': 'Custom'}

def create_link(*args):
    result = BASE_URL
    for rute in args:
        result=result+rute+'/'
    return result

def get_content(link):
    return requests.get(link,headers=HEADERS).content

def get_elemnts(soup,tag,attribute,value):
    return soup.find_all(tag,attrs={attribute : value})

def get_elemnt(soup,tag,attribute,value):
    return soup.find(tag,attrs={attribute : value})

def get_youngest_ceo(n):
    data={}
    contents=[]
    companies=[]
    url=create_link('most-active')
    content = get_content(url)

    soup = BeautifulSoup(content, 'html.parser')
    links=get_elemnts(soup,'a','data-test','quoteLink')

    for link in links:
        companies.append(link.get('href').split('=')[1])
    
    for company in companies:
        c=get_content('https://finance.yahoo.com/quote/TSLA/profile?p='+company)
        s = BeautifulSoup(c, 'html.parser')
        result=get_elemnt(s,'div','class','Mb(25px)').contents

        data['Name']=result.previous_sibling.contents[0]
        data['Code']=

        contents.append(result)
        #data{'Name':}
        break
    
    print(type(contents[0]))
    title_tag=contents[0].contents[0]
    print(title_tag)
    
    print(len(contents))
    print(companies)

if __name__ == '__main__':
    get_youngest_ceo(5)

    


