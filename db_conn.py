import sqlite3
from pathlib import Path

DB_FILEPATH = Path("ClanTool.db")

DB_CONN = sqlite3.connect(DB_FILEPATH)