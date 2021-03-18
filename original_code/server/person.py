class Person:
    """
    Represents a person, holds the name, socket client and IPaddress
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """
        set the persons name
        :param name: str
        :return: None
        """
        self.name = name

    def __repr__(self):
        return f"Person{self.addr}, {self.name}"
