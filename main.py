__author__ = 'mosquito'
import logging
from logging import Formatter, FileHandler
from amazon.api import AmazonAPI
import bottlenose.api
import urllib2
from urllib2 import URLError
from scrapy.selector import Selector
import json
import os
import sys
from time import sleep
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
                self.amazon_us = AmazonAPI(str(AMAZON_ACCESS_KEY), str(AMAZON_SECRET_KEY), str(AMAZON_ASSOC_TAG),
                                           region="US")
            else:
                LOGGER.error('Some mandatory Amazon credentials are empty. Aborting...')
                sys.exit()
        else:
            LOGGER.error('Could not find amazon_credentials_file.json file. Aborting...')
            sys.exit()

    def search_products_by_brand(self):
        """
        Call the search method of the Amazon API searching for products/sellers of a particular brand
        """
        while True:
            brand_id = raw_input("Please insert brand to extract product info from -> ")
            try:
                if brand_id and isinstance(brand_id, str):
                    row_counter = 1
                    self.products = self.amazon_us.search(Brand=brand_id, SearchIndex='Automotive')
                    '''pages = self.products.iterate_pages()
                    i = 1
                    for page in pages:
                        for product in page.Items:
                            print "{0}. '{1}'".format(i, product.title)
                            i += 1
                            sleep(0.9)
                    for i, product in enumerate(self.products):
                        print "{0}. '{1}'".format(i, product.title)
                        sleep(0.9)
                    return'''
                    excel_book = self.create_brand_excel_file(brand_id, 'products')
                    index = excel_book.get_active_sheet()
                    sheet = excel_book.get_sheet(index)
                    for i, product in enumerate(self.products):
                        print "{0}. '{1}'".format(i, product.title)
                        product_url = product.offer_url
                        final = product_url.rsplit('/', 1)
                        if product_url:
                            try:
                                #Write a line in excel file
                                sheet.write(row_counter, 0, brand_id)
                                sheet.write(row_counter, 1, product.asin)
                                sheet.write(row_counter, 2, product.editorial_review)
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

                                #Get the ASIN
                                if product.item.ASIN:
                                    sheet.write(row_counter, 15, str(product.item.ASIN))
                                else:
                                    sheet.write(row_counter, 15, 'Unknown')

                                # Get the Images from the Item
                                images_urls = []
                                if product.large_image_url:
                                    images_urls.append(product.large_image_url)
                                try:
                                    image_sets = product.item.ImageSets
                                    for image_set in image_sets:
                                        if image_set.ImageSet.LargeImage.URL:
                                            images_urls.append(str(image_set.ImageSet.LargeImage.URL))
                                    images = ', '.join(x for x in images_urls)
                                    sheet.write(row_counter, 16, images)
                                except AttributeError as e:
                                    print e.message
                                    sheet.write(row_counter, 16, 'Unknown')

                                # Get the model
                                if product.model:
                                    sheet.write(row_counter, 17, str(product.model))
                                else:
                                    sheet.write(row_counter, 17, 'Unknown')

                                # Get the publication date
                                if product.publication_date:
                                    sheet.write(row_counter, 18, str(product.publication_date))
                                else:
                                    sheet.write(row_counter, 18, 'Unknown')

                                #Get the product seller using Scrapy
                                product_file = urllib2.urlopen(product_url).read()
                                hxs = Selector(text=product_file)
                                #Get the seller
                                seller = hxs.xpath('//div[@id="merchant-info"]/a/text()').extract()
                                if seller:
                                    sheet.write(row_counter, 14, str(seller[0]))
                                    self.searched_products.append(product)
                                else:
                                    sheet.write(row_counter, 14, 'Unknown')

                                row_counter += 1
                                # Wait for 2 seconds before making another request
                                sleep(2)
                            except URLError as e:
                                sheet.write(row_counter, 14, 'Unknown')
                                print e.reason
                                row_counter += 1
                                sleep(2)
                        sleep(0.9)

                    excel_book.save(brand_id + '.xls')
                    break
                else:
                    print 'Whoops, looks like there entered a non-valid brand, it should be a text, for instance ' \
                          '"Wako industries"'
            except ValueError:
                print 'Whoops, looks like you entered a non-valid brand, must be a valid text, please try again...'

    def search_products_by_sku(self):
        print 'hey'

    def search_products_by_seller(self):
        """
        Call the search method of the Amazon API searching for sellers of a particular brand
        """
        while True:
            seller_id = raw_input("Please insert seller to extract product info from -> ")
            try:
                if seller_id and isinstance(seller_id, str):
                    row_counter = 1
                    self.products = self.amazon_us.search(Keywords=seller_id, Title='Headlights', SearchIndex='Automotive')
                    excel_book = self.create_seller_excel_file(seller_id, 'products')
                    index = excel_book.get_active_sheet()
                    sheet = excel_book.get_sheet(index)
                    for i, product in enumerate(self.products):
                        print "{0}. '{1}'".format(i, product.title)
                        product_url = product.offer_url
                        final = product_url.rsplit('/', 1)
                        if product_url:
                            #Write a line in excel file
                            sheet.write(row_counter, 0, seller_id)
                            sheet.write(row_counter, 1, product.asin)
                            sheet.write(row_counter, 2, product.editorial_review)
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

                            #Get the ASIN
                            if product.item.ASIN:
                                sheet.write(row_counter, 14, str(product.item.ASIN))
                            else:
                                sheet.write(row_counter, 14, 'Unknown')

                            # Get the Images from the Item
                            images_urls = []
                            if product.large_image_url:
                                images_urls.append(product.large_image_url)
                            try:
                                image_sets = product.item.ImageSets
                                for image_set in image_sets:
                                    if image_set.ImageSet.LargeImage.URL:
                                        images_urls.append(str(image_set.ImageSet.LargeImage.URL))
                                images = ', '.join(x for x in images_urls)
                                sheet.write(row_counter, 15, images)
                            except AttributeError as e:
                                print e.message
                                sheet.write(row_counter, 15, 'Unknown')

                            # Get the model
                            if product.model:
                                sheet.write(row_counter, 16, str(product.model))
                            else:
                                sheet.write(row_counter, 16, 'Unknown')

                            # Get the publication date
                            if product.publication_date:
                                sheet.write(row_counter, 18, str(product.publication_date))
                            else:
                                sheet.write(row_counter, 17, 'Unknown')

                            row_counter += 1
                            # Wait for 2 seconds before making another request
                            sleep(2)
                        sleep(0.9)
                    excel_book.save(seller_id + '.xls')
                    break
                else:
                    print 'Whoops, looks like there entered a non-valid brand, it should be a text, for instance ' \
                          '"Wako industries"'
            except ValueError:
                print 'Whoops, looks like you entered a non-valid brand, must be a valid text, please try again...'

    def create_brand_excel_file(self, file_name=None, sheet_name=None):
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
        col1_name = 'Brand'
        col2_name = 'ASIN'
        col3_name = 'Editorial review'
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
        col15name = 'Sold by'
        col16name = 'ASIN'
        col17name = 'Images URLs'
        col18name = 'model'
        col19name = 'Publication Date'

        style = xlwt.XFStyle()

        # font
        font = xlwt.Font()
        font.name = 'Arial'
        font.colour_index = xlwt.Style.colour_map['white']
        font.bold = True
        style.font = font

        # background color
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['dark_purple']
        style.pattern = pattern

        # borders
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders

        #Write the first row headers
        sheet.write(0, 0, col1_name, style=style)
        sheet.write(0, 1, col2_name, style=style)
        sheet.write(0, 2, col3_name, style=style)
        sheet.write(0, 3, col4_name, style=style)
        sheet.write(0, 4, col5_name, style=style)
        sheet.write(0, 5, col6_name, style=style)
        sheet.write(0, 6, col7_name, style=style)
        sheet.write(0, 7, col8_name, style=style)
        sheet.write(0, 8, col9_name, style=style)
        sheet.write(0, 9, col10_name, style=style)
        sheet.write(0, 10, col11_name, style=style)
        sheet.write(0, 11, col12_name, style=style)
        sheet.write(0, 12, col13_name, style=style)
        sheet.write(0, 13, col14_name, style=style)
        sheet.write(0, 14, col15name, style=style)
        sheet.write(0, 15, col16name, style=style)
        sheet.write(0, 16, col17name, style=style)
        sheet.write(0, 17, col18name, style=style)
        sheet.write(0, 18, col19name, style=style)
        book.save(excel_name)
        return book

    def create_seller_excel_file(self, file_name=None, sheet_name=None):
        """
        A helper method that creates a excel file for a seller products
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
        col1_name = 'Brand'
        col2_name = 'ASIN'
        col3_name = 'Editorial review'
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
        col15name = 'ASIN'
        col16name = 'Images URLs'
        col17name = 'model'
        col18name = 'Publication Date'

        style = xlwt.XFStyle()

        # font
        font = xlwt.Font()
        font.name = 'Arial'
        font.colour_index = xlwt.Style.colour_map['white']
        font.bold = True
        style.font = font

        # background color
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['dark_purple']
        style.pattern = pattern

        # borders
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders

        #Write the first row headers
        sheet.write(0, 0, col1_name, style=style)
        sheet.write(0, 1, col2_name, style=style)
        sheet.write(0, 2, col3_name, style=style)
        sheet.write(0, 3, col4_name, style=style)
        sheet.write(0, 4, col5_name, style=style)
        sheet.write(0, 5, col6_name, style=style)
        sheet.write(0, 6, col7_name, style=style)
        sheet.write(0, 7, col8_name, style=style)
        sheet.write(0, 8, col9_name, style=style)
        sheet.write(0, 9, col10_name, style=style)
        sheet.write(0, 10, col11_name, style=style)
        sheet.write(0, 11, col12_name, style=style)
        sheet.write(0, 12, col13_name, style=style)
        sheet.write(0, 13, col14_name, style=style)
        sheet.write(0, 14, col15name, style=style)
        sheet.write(0, 15, col16name, style=style)
        sheet.write(0, 16, col17name, style=style)
        sheet.write(0, 17, col18name, style=style)
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






