class DataEntry:
    """
    Base class for all devices
    """
    def __init__(self, module, name):
        self.module = module
        self.name = name

    def get_name(self):
        return f"{self.name}"
