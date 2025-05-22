# backend/db_connection.py

import mysql.connector
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (si tu utilises .env)
load_dotenv()

def get_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "quran_school_db")
    )
    return connection
