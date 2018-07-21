# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 19:42:00 2018

@author: 30989
"""
#%%
from __future__ import print_function
import datetime
from math import ceil
import bs4
import pymysql.cursors
import requests

#%%
def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P500
    constituents using requests and BeautifulSoup.
    
    Returns a list of tuples for adding to MySQL.
    """
    #Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()
    
    """
    Use requests and Beautifulsoup to download the list of S&P500 companies
    and obtain the symbol table
    """
    response = requests.get(
            "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs4.BeautifulSoup(response.text)
    
    """
    This selects the first table, using CSS Selector syntax and then ignores
    the header row([1:])
    """
    symbolslist = soup.select('table')[0].select('tr')[1:]
    
    """
    Obtain the symbol information for each row in the S&P500 constituent
    table
    """
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
                (
                        tds[0].select('a')[0].text, #Ticker
                        'stock',
                        tds[1].select('a')[0].text, #Name
                        tds[3].text, # Sector
                        'USD', now, now
                        ))
    return symbols
    
    
    
    
#%%
#def insert_snp500_symbols(symbols):
#    """
#    Insert the S&P500 symbols into the MySQL database.
#    """
#    
#    connection = pymysql.connect(host='localhost',
#                            user='root',
#                             port=3306,
#                             password='',
#                             db='securities_master',
#                             cursorclass=pymysql.cursors.DictCursor)
#    #Connect to the MySQL instance
#    #column_str="ticker, instrument, name, sector,currency, created_date, last_updated_date"
#               
#                  
#    #insert_str = ("%s, " * 7)[:-2]
#    
#    try:
#        with connection.cursor() as cursor:
#            sqlQuery =  "INSERT INTO symbol(`ticker`, `instrument`, `name`, `sector`, `currency`, `created_date`,'last_updated_date') VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
#            cursor.execute(sqlQuery, (symbols))
#            connection.commit()
#            
#                       
#                         
#            
#    finally:
#        connection.close()
#    
#    
    
        
        

    
    
   
    
    
    

  
    
    
    
    
    
      
        
    
    
        
        
        
        
                                                                                                                                                         
#%%
if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    connection = pymysql.connect(host='localhost',
                            user='root',
                             port=3306,
                             password='',
                             db='securities_master',
                             cursorclass=pymysql.cursors.DictCursor)
    vals = symbols
    try:
        with connection.cursor() as cursor:
        cursor.executemany("insert into symbol(ticker,instrument,name,sector,currency,created_date,last_updated_date) values (%s, %s,%s,%s,%s,%s,%s)", vals )
        
        connection.commit()
        
   finally:
          connection.close()
    
             
             
             
        
   
      
        
   