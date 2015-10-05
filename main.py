__author__ = 'mosquito'
import logging
from logging import Formatter, FileHandler
from amazon.api import AmazonAPI
import bottlenose.api
from urllib2 import URLError
import urllib
import json
import os
import sys
import xlwt
from view.button import Button
from view.menu import Menu
from controler.controler import Controller

#Setup the logger
LOGGER = logging.getLogger('amazon_advertising_app')
file_handler = FileHandler('amazon_advertising_app.log')
handler = logging.StreamHandler()
file_handler.setFormatter(Formatter(
    '%(thread)d %(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setFormatter(Formatter(
    '%(thread)d %(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
LOGGER.addHandler(file_handler)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)

#Constant variables
AMAZON_ACCESS_KEY = ''
AMAZON_SECRET_KEY = ''
AMAZON_ASSOC_TAG = ''
KEYWORDS = '2LHP-RAM02JM-TM'


class Main(object):
    """
    A class that gives access to this test application
    """

    #The list of products obtained
    searched_products = list()
    products = None

    def __init__(self):
        self.region_options = bottlenose.api.SERVICE_DOMAINS.keys()
        #Check if we have credentials stored, if so, load them
        if os.path.isfile('amazon_credentials.json'):
            LOGGER.info('Getting Amazon credentials from stored file...')
            credentials = json.load(open("amazon_credentials.json"))
            AMAZON_ACCESS_KEY = credentials['amazon_access_key']
            AMAZON_SECRET_KEY = credentials['amazon_secret_key']
            AMAZON_ASSOC_TAG = credentials['amazon_assoc_tag']
            if AMAZON_SECRET_KEY and AMAZON_ACCESS_KEY and AMAZON_ASSOC_TAG:
                LOGGER.info('Got Amazon credentials!')
                self.amazon_us = AmazonAPI(str(AMAZON_ACCESS_KEY), str(AMAZON_SECRET_KEY), str(AMAZON_ASSOC_TAG), region="US")
            else:
                LOGGER.error('Some mandatory Amazon credentials are empty. Aborting...')
                sys.exit()
        else:
            LOGGER.error('Could not find amazon_credentials_file.json file. Aborting...')
            sys.exit()

    def search_products_by_brand(self):
        """
        Call the search method of the Amazon API searching for sellers of a particular brand
        """
        while True:
            brand_id = raw_input("Please insert brand to extract product info from -> ")
            try:
                if brand_id and isinstance(brand_id, str):
                    row_counter = 1
                    self.products = self.amazon_us.search(Keywords=brand_id, SearchIndex='All')
                    excel_book = self.create_excel_file('products', 'products')
                    index = excel_book.get_active_sheet()
                    sheet = excel_book.get_sheet(index)
                    for i, product in enumerate(self.products):
                        print "{0}. '{1}'".format(i, product.title)
                        product_url = product.offer_url
                        final = product_url.rsplit('/', 1)
                        if product_url:
                            try:
                                #Write a line in excel file
                                sheet.write(row_counter, 0, KEYWORDS)
                                sheet.write(row_counter, 1, product.asin)
                                sheet.write(row_counter, 2, product.brand)
                                sheet.write(row_counter, 3, product.label)
                                sheet.write(row_counter, 4, str(product.list_price))
                                sheet.write(row_counter, 5, product.manufacturer)
                                sheet.write(row_counter, 6, product.mpn)
                                sheet.write(row_counter, 7, product.offer_url)
                                sheet.write(row_counter, 8, product.part_number)
                                sheet.write(row_counter, 9, str(product.price_and_currency))
                                sheet.write(row_counter, 10, product.publisher)
                                sheet.write(row_counter, 11, product.sales_rank)
                                sheet.write(row_counter, 12, product.sku)
                                sheet.write(row_counter, 13, product.title)
                                row_counter += 1

                                #req = urllib2.Request(final[0])
                                #response = urllib2.urlopen(req)
                                urllib.urlretrieve(final[0], "temp.html")
                                #Check if the G forceusa string is in the response
                                has_small_string = False
                                f = open('temp.html', 'r')
                                for line in f:
                                    if 'G Forceusa' in line:
                                        has_small_string = True
                                        break
                                if has_small_string:
                                    print 'found G forceusa!'
                                    self.searched_products.append(product)
                                #delete temp file
                                os.remove('temp.html')
                                #print response.info()   # print respose headers
                                #print response.read()   # print response content
                            except URLError as e:
                                print e.reason

                    excel_book.save(brand_id)
                    break
                else:
                    print 'Whoops, looks like there entered a non-valid brand, it should be a text, for instance ' \
                          '"Wako industries"'
            except ValueError:
                print 'Whoops, looks like you entered a non-valid brand, must be a valid text, please try again...'



    def search_products_by_sku(self):
        print 'hey'

    def search_products_by_seller(self):
        print 'hey'


    def create_excel_file(self, file_name=None, sheet_name=None):
        """
        A helper method that creates a excel file for products
        :rtype : Workbook
        :return: The excel object with the header row inserted
        """
        book = xlwt.Workbook()
        excel_name = file_name + '.xls'
        #delete the file if already exists
        if os.path.isfile(excel_name):
            os.remove(excel_name)

        sheet_name = sheet_name
        sheet = book.add_sheet(sheet_name)
        col1_name = 'SKU/Keyword'
        col2_name = 'ASIN'
        col3_name = 'Brand'
        col4_name = 'Label'
        col5_name = 'List price'
        col6_name = 'Manufacturer'
        col7_name = 'mpn'
        col8_name = 'url'
        col9_name = 'part number'
        col10_name = 'Price and currency'
        col11_name = 'Publisher'
        col12_name = 'Sales rank'
        col13_name = 'SKU'
        col14_name = 'Title'

        #Write the first row headers
        sheet.write(0, 0, col1_name)
        sheet.write(0, 1, col2_name)
        sheet.write(0, 2, col3_name)
        sheet.write(0, 3, col4_name)
        sheet.write(0, 4, col5_name)
        sheet.write(0, 5, col6_name)
        sheet.write(0, 6, col7_name)
        sheet.write(0, 7, col8_name)
        sheet.write(0, 8, col9_name)
        sheet.write(0, 9, col10_name)
        sheet.write(0, 10, col11_name)
        sheet.write(0, 11, col12_name)
        sheet.write(0, 12, col13_name)
        sheet.write(0, 13, col14_name)
        book.save(excel_name)
        return book

    def show_menu(self):
        """
        Creates the menu
        """
        menu_option_search_by_brand = Button("Search by brand", self.search_products_by_brand, 1)
        menu_option_search_by_sku = Button("Search by SKU or MPN", self.search_products_by_sku, 2)
        menu_option_search_by_seller = Button("Search by seller", self.search_products_by_seller, 3)
        menu_option_quit = Button("Quit", self.quit, 0)

        main_menu_buttons = [menu_option_search_by_brand, menu_option_search_by_sku, menu_option_search_by_seller,
                             menu_option_quit]

        main_menu = Menu(main_menu_buttons)
        controller = Controller(main_menu)
        controller.cycle()

    def quit(self):
        """
        Displays all the adverts in screen and when done shows the menu again
        """
        print('Bye, we will miss you :(!')
        sys.exit()

if __name__ == '__main__':
    app = Main()
    app.show_menu()






