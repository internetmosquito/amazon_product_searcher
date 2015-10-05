__author__ = 'mosquito'


class Menu(object):
    """
    Represents the menu object to be displayed
    """
    def __init__(self, menu=None):
        if menu is None:
            self.menu_list = []
        else:
            if type(menu) is list:
                self.menu_list = menu
                self.menu_dict = {}
                # Initialise values
                for button in menu:
                    self.menu_dict[button.nav] = button
            else:
                self.menu_list = []
                self.menu_dict = {}

    def display(self):
        """
        Displays the menu alongside the navigation elements
        """
        response = None
        while response is None:
            # Display menu buttons -- use the list so we get the same
            # order every time.
            print '******* MAIN MENU **********'
            print '****************************'
            for button in self.menu_list:
                print str(button.nav) + '.-', button.name

            # Wait for user input
            response = self.user_input()

    def user_input(self):
        """
        Method that gets user input and acts accordingly
        """
        input_sel = raw_input("Please enter a menu selection -> ")
        try:
            # Here we use the dictionary for ease of lookup, to get the corresponding button instance
            button = self.menu_dict[int(input_sel)]
        except (KeyError, ValueError):
            # The user's selection didn't match any of the button.nav
            # values, so we got a KeyError exception on the dictionary
            print 'Please insert a valid menu option...'
            return None

        button.do()
        return input_sel