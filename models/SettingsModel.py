import sys
from datetime import datetime

class SettingsModel():
    def __init__(self, server, port, user, password, database, host):
        self.server = server
        self.port = port 
        self.user = user
        self.password = password
        self.database = database
        self.host = host
