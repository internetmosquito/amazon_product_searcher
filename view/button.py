__author__ = 'mosquito'


class Button(object):
    """
    Represents a menu Button, the choice made by the user
    """
    def __init__(self, name, func, nav):
        # Initialize values
        self.name = name
        # Function associated with button. the one that will be executed
        self.func = func
        # Navigation element; the menu number basically
        self.nav = nav

    def do(self):
        """
        Simply calls the passed function
        """
        # Do the button's function
        self.func()

