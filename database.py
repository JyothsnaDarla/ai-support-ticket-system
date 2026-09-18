import os
import sqlite3
import pandas as pd

DB_FILE = "tickets.db"


def init_db(csv_path="support_tickets.csv"):
  """Initializes the SQLite database from a CSV file if it exists."""
  if not os.path.exists(csv_path):
    print(
        f"Warning: '{csv_path}' not found. Skipping database table initialization."
    )
    return

  df = pd.read_csv(csv_path)
  conn = sqlite3.connect(DB_FILE)
  df.to_sql("tickets", conn, if_exists="replace", index=False)
  conn.close()
  print("Database initialized successfully.")


def execute_query(sql_query: str):
  """Executes a raw SQL query and returns results as a dictionary list."""
  conn = sqlite3.connect(DB_FILE)
  try:
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df.to_dict(orient="records"), None
  except Exception as e:
    conn.close()
    return None, str(e)


if __name__ == "__main__":
  init_db()