# from pathlib import Path
#
#
# home = str(Path.home())
import os
home = os.path.dirname(os.path.abspath(__file__))

# constants
PORT = 14908
ENCODING = 'utf-8'

# DataBase
DB_PROTOCOL = 'sqlite:///'
DB_NAME = '/server_contacts.db'
DB_PATH = DB_PROTOCOL + home + DB_NAME
