from bs4 import BeautifulSoup
import requests
from abc import ABC,abstractmethod
import pymysql
import time
import random
from AbstractClass import *

URL = 'https://www.avito.ru/rossiya/avtomobili?cd='

class ParserConnectWithDatabaseAvito(ParserConnectWithDatabase):

    def InsertingIntoTable(self, all):
        with self.connection.cursor() as cursor:
            try:
                sql_querry = 'insert into avito(Location, NameCar, Comments, GoodPrice, Link, Price, Picture) values (%s, %s ,%s ,%s ,%s ,%s, %s)'
                for volume in range(len(all['Price'])):
                    val = (
                        str(all['Location'][volume]),
                        str(all['NameCar'][volume]),
                        str(all['Comments'][volume][0:230]),
                        str(all['GoodPrice'][volume]),
                        str(all['Link'][volume]),
                        int(all['Price'][volume]),
                        str(all['Picture'][volume])
                    )
                    cursor.execute(sql_querry,val)
                self.connection.commit()
                print('In table insert data...')
            except Exception as ex:
                print('Error in Insert Into Database ' + str(ex))

class ParserAvito(ParserWebsite):
    def __init__(self, url):
        self.location = []
        self.nameCar = []
        self.comments = []
        self.goodPrice = []
        self.link = []
        self.price = []
        self.picture = []
        super().__init__(url)

    def parsing(self):
        self.boss_Tag = self.soup.findAll('div', itemtype='http://schema.org/Product')

        for tag in self.boss_Tag:
            price = tag.find('meta', itemprop='price')
            self.appendingInListMode(self.price, price, 'get', 'content')
            location = tag.find('div', class_='geo-root-zPwRk iva-item-geo-_Owyg')
            self.appendingInListMode(self.location, location, 'text')
            nameCar = tag.find('h3', itemprop='name')
            self.appendingInListMode(self.nameCar, nameCar, 'text')
            comments = tag.find('div', class_='iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL')
            self.appendingInListMode(self.comments, comments, 'text')
            goodPrice = tag.find('div', class_='SnippetBadgeBar-root-B6Bj3')
            self.appendingInListMode(self.goodPrice, goodPrice, 'text')
            link = tag.find('a', itemprop='url')
            self.link.append('https://www.avito.ru' + link.get('href'))
            picture = tag.find('img', itemprop='image', class_='photo-slider-image-YqMGj')
            self.appendingInListMode(self.picture, picture, 'get', 'src')
    def return_all(self):
        all = {
            'Price': self.price,
            'Location': self.location,
            'NameCar': self.nameCar,
            'Comments': self.comments,
            'GoodPrice': self.goodPrice,
            'Link': self.link,
            'Picture': self.picture,
        }
        return all

class ParserMainAvito():
    def parser_main_avito(self,page_count,delete_table = 0):
        connect = ParserConnectWithDatabaseAvito
        connect.ConnectingDataBase(connect)
        if delete_table == 1:
            connect.DropingTable(connect)
            connect.CreatingTable(connect)

        count = 1
        while(count < page_count):
            parsing = ParserAvito(URL + str(count))
            parsing.parsing()
            connect.InsertingIntoTable(connect, parsing.return_all())
            value = random.random()
            scaled_value = 1 + (value * (9 - 5))
            time.sleep(scaled_value)
            count +=1