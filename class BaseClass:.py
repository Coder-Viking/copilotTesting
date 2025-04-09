class BaseClass:
    def __init__(self):
        """
        Constructor for the BaseClass.
        Initialize any default attributes here.
        """
        self.name = "BaseClass"
        self.version = 1.0

    def display_info(self):
        """
        Display basic information about the class.
        """
        print(f"Class Name: {self.name}")
        print(f"Version: {self.version}")

    def run(self):
        """
        Placeholder method to be overridden by subclasses.
        """
        print("Running the base class. Override this method in a subclass.")