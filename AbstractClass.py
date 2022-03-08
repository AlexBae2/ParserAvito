from abc import abstractmethod
import requests
from bs4 import BeautifulSoup
import pymysql

class ParserConnectWithDatabase():
    def ConnectingDataBase(self):
        try:
            self.connection = pymysql.connect(
                host="localhost",
                user="root",
                database="db",  # database
                passwd="_q_qqsssanvarqqqss_s_"
            )
            print("Successfully connected...")
        except Exception as ex:
            print('Error in ConnectingDataBase ' + str(ex))

    def CreatingTable(self):
        with self.connection.cursor() as cursor:
            try:
                create_table_querry = "" \
                                      "CREATE TABLE avito(" \
                                      "Id INTEGER AUTO_INCREMENT PRIMARY KEY," \
                                      "Location varchar (256)," \
                                      "NameCar varchar(256)," \
                                      "Comments VARCHAR(256)," \
                                      "GoodPrice varchar(256)," \
                                      "Link varchar(256)," \
                                      "Price int," \
                                      "Picture varchar (512))"
                cursor.execute(create_table_querry)
                print('Table created...')
            except Exception as ex:
                print('Error in Creating Table ' + str(ex))

    def DropingTable(self):
        with self.connection.cursor() as cursor:
            try:
                drop_database_querry = "DROP TABLE avito"
                cursor.execute(drop_database_querry)
                print('Table was dropped...')
            except Exception as ex:
                print('Error in Dropping Table ' + str(ex))
    @abstractmethod
    def InsertingIntoTable(self):
        pass

class ParserWebsite:
    def __init__(self,url,headers = ''):
        self.url = url
        if len(headers) != 0:
            response = requests.get(url,headers = headers)
        else:
            response = requests.get(url)
        response.encoding = 'utf8'
        self.soup = BeautifulSoup(response.text, 'lxml')

    def encoding_ascii(self, encode, mode = '0'):
        if encode != None and mode == '0':
            encode = str(encode).encode("ascii", "ignore")
            decode = encode.decode()
        elif encode != None and mode == 'text':
            encode = str(encode.text).encode("ascii", "ignore")
            decode = encode.decode()
        else:
            decode = 'None'
        return decode

    def appendingInListMode(self, list, soup_list, mode, atr = 0, All = False):
        if mode == 'get' and soup_list != None and All == False:
            list.append(soup_list.get(atr))
        elif mode == 'text' and soup_list != None and All == False:
            list.append(soup_list.text)
        elif mode == 'text' and soup_list != None and All == True:
            full_str = ''
            for unit in soup_list:
                full_str +=unit.text + ' '
            list.append(full_str)
        else:
            list.append('None')
