import os
import sqlite3
from app import Database
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        Database.DB_NAME = ":memory:"
        Database.init_db()
        
    def test_init_create_db(self):
        conn = sqlite3.connect(Database.DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contact'")
        table = cur.fetchone()
        conn.close()
        self.assertIsNotNone(table, "Contact table should exist")
        
    def test_contact_insertion(self):
        Database.save_contact("TestUser", "test@gmail.com", "Hello")
        
        conn = sqlite3.connect(Database.DB_NAME)
        cur = conn.cursor()
        cur.execute("SELET * FROM contact")
        result = cur.fetchall()
        conn.close()
        self.assertEqual(len(result), 1, "One contact should have been inserted")
        
        
if __name__ == "__main__":
    unittest.main()
        