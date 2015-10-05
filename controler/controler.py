__author__ = 'mosquito'


class Controller(object):
    """
    A class to act as the controler for the view and model
    """
    def __init__(self, menu):
        # Initialize values
        self.menu = menu
        # Start menu displaying / cycling
        self.cycle()

    def cycle(self):
        """
        A method that displays the menu constantly until the user is bored to death or selects the Exit option :D
        """
        while True:
            self.menu.display()