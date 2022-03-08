from bs4 import BeautifulSoup
import requests
from abc import ABC,abstractmethod
import pymysql
import time
import random
from AbstractClass import *

URL = 'https://auto.ru/rossiya/cars/used/?page='
USER_AGENT = {
'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.116 YaBrowser/22.1.1.1544 Yowser/2.5 Safari/537.36'
}

class ParserConnectWithDatabaseAvito(ParserConnectWithDatabase):
    def InsertingIntoTable(self, all):
        with self.connection.cursor() as cursor:
            try:
                sql_querry = 'insert into avito(Location, NameCar, Comments, GoodPrice, Link, Price) values (%s, %s ,%s ,%s ,%s ,%s)'
                for volume in range(len(all['Price'])):
                    val = (
                        str(all['Location'][volume]),
                        str(all['NameCar'][volume]),
                        str(all['Comments'][volume][0:230]),
                        str(all['GoodPrice'][volume]),
                        str(all['Link'][volume]),
                        int(all['Price'][volume])
                    )
                    cursor.execute(sql_querry,val)
                self.connection.commit()
                print('In table insert data...')
            except Exception as ex:
                print('Error in Insert Into Database ' + str(ex))

class ParserAutoRu(ParserWebsite):
    def __init__(self, url,headers):
        self.location = []
        self.nameCar = []
        self.comments = []
        self.goodPrice = []
        self.link = []
        self.price = []
        super().__init__(url,headers)
    def parsing(self):
        self.boss_Tag = self.soup.findAll('div', class_='ListingItem')

        for tag in self.boss_Tag:
            unsorted_price = tag.find('div', class_='ListingItemPrice__content')
            if unsorted_price != None:
                unsorted_price = unsorted_price.get_text().replace(u'\xa0',u' ')# удаляем скрытые пробелы
                price = ''
                for x in unsorted_price:
                    for i in x:
                        if i.isdigit():
                            price += i
                self.price.append(int(price))
            location = tag.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp')
            self.appendingInListMode(self.location, location, 'text')
            nameCar = tag.find('div', class_='ListingItem__columnCellSummary')
            self.nameCar.append(self.encoding_ascii(nameCar,mode = 'text'))
            comments = tag.findAll('div',class_='ListingItemTechSummaryDesktop__cell')
            self.appendingInListMode(self.comments, comments, 'text', All=True)
            goodPrice = tag.find('div', class_='OfferPriceBadge OfferPriceBadge_good')
            self.appendingInListMode(self.goodPrice, goodPrice, 'text')
            link = tag.find('a', class_='Link ListingItemTitle__link')
            self.appendingInListMode(self.link, link, 'get','href')

    def return_all(self):
        all = {
            'Price': self.price,
            'Location': self.location,
            'NameCar': self.nameCar,
            'Comments': self.comments,
            'GoodPrice': self.goodPrice,
            'Link': self.link,
        }
        return all

class ParserMainAutoRu():
    def parser_main_autoru(self,page_count,delete_table = 0):

        connect = ParserConnectWithDatabaseAvito
        connect.ConnectingDataBase(connect)
        if delete_table == 1:
            connect.DropingTable(connect)
            connect.CreatingTable(connect)

        count = 1
        while(count < page_count):
            parsing = ParserAutoRu(URL + str(count),USER_AGENT)
            parsing.parsing()
            print(parsing.boss_Tag)
            connect.InsertingIntoTable(connect, parsing.return_all())
            value = random.random()
            scaled_value = 1 + (value * (9 - 5))
            time.sleep(scaled_value)
            count +=1