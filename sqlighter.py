import sqlite3

class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
    
    def get_channels(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'scraper_channel'").fetchall()
    
    def get_profiles(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'scraper_profile'").fetchall()
            