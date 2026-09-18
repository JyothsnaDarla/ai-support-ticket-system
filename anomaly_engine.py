import os
import sqlite3
import pandas as pd


def detect_anomalies():
  """Detects SLA breaches and statistical resolution time outliers."""
  if not os.path.exists("tickets.db"):
    return []

  conn = sqlite3.connect("tickets.db")
  try:
    df = pd.read_sql_query("SELECT * FROM tickets", conn)
  except Exception:
    conn.close()
    return []
  conn.close()

  if df.empty:
    return []

  anomalies = []

  # Rule 1: Unresolved High/Critical tickets > 24 hours
  df["created_at"] = pd.to_datetime(df["created_at"])
  now = df["created_at"].max()  # Baseline reference using dataset max date

  unresolved_mask = (
      (df["status"] != "Resolved")
      & (df["priority"].isin(["High", "Critical"]))
      & (((now - df["created_at"]).dt.total_seconds() / 3600) > 24)
  )

  for _, row in df[unresolved_mask].iterrows():
    anomalies.append({
        "ticket_id": row["ticket_id"],
        "type": "SLA Breach",
        "reason": f"Unresolved {row['priority']} ticket older than 24h",
    })

  # Rule 2: Statistical Outliers in Resolution Time (> 2 * std_dev)
  resolved_df = df[df["resolution_time_hrs"].notnull()]
  if not resolved_df.empty:
    mean_res = resolved_df["resolution_time_hrs"].mean()
    std_res = resolved_df["resolution_time_hrs"].std()
    cutoff = mean_res + (2 * std_res)

    outliers = resolved_df[resolved_df["resolution_time_hrs"] > cutoff]
    for _, row in outliers.iterrows():
      anomalies.append({
          "ticket_id": row["ticket_id"],
          "type": "High Resolution Time",
          "reason": (
              f"Resolution time ({row['resolution_time_hrs']} hrs) exceeds"
              f" statistical threshold ({cutoff:.1f} hrs)"
          ),
      })

  return anomalies