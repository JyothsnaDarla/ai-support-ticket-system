import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Support Ticket System", layout="wide")
st.title("🎫 AI Support System Analytics")

tab1, tab2 = st.tabs(["Natural Language Query", "Anomaly Dashboard"])

with tab1:
  st.subheader("Ask a Question")
  user_query = st.text_input(
      "Query", "Which agent has the lowest average customer rating?"
  )

  if st.button("Submit"):
    try:
      response = requests.post(
          f"{API_URL}/query", json={"query": user_query}, timeout=10
      )
      response.raise_for_status()
      res = response.json()

      if "result" in res:
        st.code(res.get("sql_generated", ""), language="sql")
        st.write(res.get("explanation", ""))
        st.dataframe(res["result"])
      else:
        st.error("Error processing request.")

    except requests.exceptions.RequestException as e:
      st.error(f"Failed to connect to API backend: {e}")

with tab2:
  st.subheader("System Flagged Anomalies")
  if st.button("Scan Anomalies"):
    try:
      response = requests.get(f"{API_URL}/anomalies", timeout=10)
      response.raise_for_status()
      res = response.json()

      if "anomalies" in res:
        st.dataframe(res["anomalies"])
      else:
        st.warning("No anomaly key returned from backend response.")

    except requests.exceptions.RequestException as e:
      st.error(f"Failed to fetch anomalies: {e}")