__author__ = 'mosquito'


import unittest
from model.model import User, Advert
from main import Main


class GeneralTests(unittest.TestCase):

    ###############
    #### tests ####
    ###############
    def test_user_creation(self):
        #Check if user with wrong email is created correctly
        self.assertRaises(Exception, User, '12345')
        user = User()
        self.assertIs(user.email, 'Unknown')
        another_user = User('john.doe@acme.com')
        self.assertIs(another_user.email, 'john.doe@acme.com')

    def test_adverts_creation(self):
        #Check if advert counter is working correctly first
        advert1 = Advert(None, None, None)
        advert2 = Advert(None, None, None)
        self.assertIs(advert1.id, 0)
        self.assertIs(advert2.id, 1)
        #Check owner of created adverts is assigned correctly to adverts
        user = User('john.doe@acme.com')
        advert3 = Advert(user, None, None)
        self.assertIs(advert3.owner, 'Unknown')
        advert4 = Advert(user.email, None, None)
        self.assertIs(advert4.owner, user.email)
        #Let's see what happens when we pass invalid prices and quantities
        advert5 = Advert(user.email, 'aaa', 'bbb')
        self.assertEquals(advert5.price, 0.0)
        self.assertEquals(advert5.quantity, 0)
        #Create a good one and see that everything is OK
        advert6 = Advert(user.email, 23.15, 2)
        self.assertIs(advert6.owner, user.email)
        self.assertEquals(advert6.price, 23.15)
        self.assertEquals(advert6.quantity, 2)

    def test_main_app_creates_three_dummy_objects(self):
        #Check that when created, the Main object only contains 3 ads
        main = Main()
        self.assertEquals(len(main.adverts_list), 3)

    def test_main_app_shows_adverts_menu(self):
        #Check that the output from the menu for the first option displays the 3 elements created at statup
        main = Main()
        ads = main.construct_adverts()
        self.assertEqual(ads.count("ID"), 3)
        #Now delete the adverts and make sure there is none
        main.adverts_list = []
        ads = main.construct_adverts()
        self.assertEqual(ads.count("ID"), 0)

    def test_updated_events_get_correctly_updated(self):
        #Checks that constructed adverts can get price and quantity modified correctly
        main = Main()
        advert = main.adverts_list[0]
        old_price = advert.price
        old_quantity = advert.quantity
        advert = main.update_advert(advert, 'price', 99.99)
        self.assertNotEqual(advert.price, old_price)
        advert = main.update_advert(advert, 'quantity', 10)
        self.assertNotEqual(advert.quantity, old_quantity)

    def test_events_with_updates_get_modifications(self):
        #Checks that updated adverts have correct modifications
        main = Main()
        advert = main.adverts_list[0]
        old_price = advert.price
        old_quantity = advert.quantity
        advert = main.update_advert(advert, 'price', 99.99)
        self.assertNotEqual(advert.price, old_price)
        advert = main.update_advert(advert, 'quantity', 10)
        self.assertNotEqual(advert.quantity, old_quantity)
        mod_list = main.modifications_dict[advert.id]
        self.assertEqual(len(mod_list), 2)
        mod = mod_list[0]
        self.assertEqual(mod.price, advert.price)






