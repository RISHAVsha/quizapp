"""from flask import g, current_app
import sqlite3
import os

def connect_db():
    db_path = os.path.join(current_app.instance, 'quizapp.db')
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    return sqlite3.connect(db_path)

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
"""