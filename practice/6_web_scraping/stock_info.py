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
| Name        | Code | Country       | Employees | CEO Name                             |  |
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
from operator import itemgetter
from rich.console import Console
from rich.table import Table

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

def filter_CEO(span):
    return span and re.compile("CEO").search(span)

def print_data(title,colums,rows):
    table=Table(title='====================== '+title+' ======================')

    for colum in colums:
        table.add_column(colum,justify="left")
    
    for row in rows:
        x=list(row.values())
        table.add_row(*x)
        table.add_row()
    
    console = Console()
    console.print(table)

def get_companies():
    codes = []
    names = []

    url=create_link('most-active')
    content = get_content(url)

    soup = BeautifulSoup(content, 'html.parser')
    links=get_elemnts(soup,'a','data-test','quoteLink')

    for link in links:
        codes.append(link.get('href').split('=')[1])
    
    names_list = get_elemnts(soup,'td','aria-label','Name')

    for name in names_list:
        names.append(name.string)

    return codes,names

def get_youngest_ceo(n,codes,names):
    contents=[]
    i=-1

    for company in codes:
        i=i+1
        data={}
        c=get_content('https://finance.yahoo.com/quote/'+company+'/profile?p='+company)
        s = BeautifulSoup(c, 'html.parser')
        
        info=get_elemnt(s,'div','class','Mb(25px)')
    
        data['Name'] = names[i]
        data['Code'] = company
        data['Country'] = list(info.contents[0].descendants)[-7]

        employees=list(info.contents[1].descendants)[-1]

        try:
            employees=employees.replace(',','')
            data['Employees'] = employees
        except:
            data['Employees'] = ' '

        ceo_data= get_elemnt(s,'table','class','W(100%)')

        try:
            row=ceo_data.contents[1].find_all(string=re.compile("CEO"))[0].find_previous('tr')
            data['CEO Name'] = list(row.contents[0].descendants)[-1]
            data['CEO Year Born'] = list(row.contents[-1].descendants)[-1]
        except:
            data['CEO Name'] = ''
            data['CEO Year Born'] = '0'

        contents.append(data)
    
    newlist = sorted(contents, key=lambda d: int(d['CEO Year Born']), reverse=True)
    colums=newlist[0].keys()
    print_data('5 stocks with most youngest CEOs',colums,newlist[:n])

    return(newlist[:n])

def stocks_best_52_Week_Change(n,codes,names):
    contents=[]
    i=-1

    for company in codes:
        i=i+1
        data={}
        c=get_content('https://finance.yahoo.com/quote/'+company+'/key-statistics?p='+company)
        s = BeautifulSoup(c, 'html.parser')
         
        data['Name'] = names[i]
        data['Code'] = company

        row=s.contents[1].find_all(string=re.compile("52-Week Change"))[0].find_previous('tr')
        data['52-Week Change'] = list(row.descendants)[-1]

        row=s.contents[1].find_all(string=re.compile("Total Cash"))[0].find_previous('tr')
        data['Total Cash'] = list(row.descendants)[-1]
        contents.append(data)
    
    newlist = sorted(contents, key=lambda d: float(d['52-Week Change'][:-1]), reverse=True)
    colums=newlist[0].keys()
    print_data('10 stocks with best 52-Week Change',colums,newlist[:n])

    return(newlist[:n])

def largest_holds_of_Blackrock(n,codes,names):
    contents=[]
    i=-1

    for company in codes:
        i=i+1
        data={}
        c=get_content('https://finance.yahoo.com/quote/'+company+'/holders?p='+company)
        s = BeautifulSoup(c, 'html.parser')
         
        data['Name'] = names[i]
        data['Code'] = company

        try:
            row=s.contents[1].find_all(string=re.compile("Blackrock Inc"))[0].find_previous('tr')
            strings = row.find_all(string=True)

            data['Shares'] = strings[1]
            data['Date Reported'] = strings[2]
            data['Out'] = strings[3]
            data['Value'] = strings[4]
        except:
            data['Shares'] = ''
            data['Date Reported'] = ''
            data['Out'] = ''
            data['Value'] = '0'

        contents.append(data)
    
    newlist = sorted(contents, key=lambda d: int(d['Value'].replace(',','')), reverse=True)
    colums=newlist[0].keys()
    print_data('10 largest holds of Blackrock Inc.',colums,newlist[:n])

    return(newlist[:n])

if __name__ == '__main__':
    companies,names=get_companies()
    get_youngest_ceo(5,companies,names)
    stocks_best_52_Week_Change(10,companies,names)
    largest_holds_of_Blackrock(10,companies,names)