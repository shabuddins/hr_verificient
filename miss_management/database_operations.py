import sqlite3
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
cursor = db.cursor()

# cursor.execute('delete from Emp_goal_data_man where emp_id = ?', (23,))
cursor.execute('show tables')
print(cursor.fetchall())