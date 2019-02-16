import sys
from datetime import datetime

class AppInfoModel():
    def __init__(self, name, description, publisher, version, license):
        self.name = name
        self.description = description 
        self.publisher = publisher
        self.version = version
        self.license = license