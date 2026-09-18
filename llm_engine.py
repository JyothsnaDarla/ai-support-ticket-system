import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """You are an expert SQLite query generator.
Convert the user request into a single valid SQLite query for table `tickets`.
Return ONLY raw executable SQL code. Do NOT include explanations, markdown formatting, backticks, or conversational text.

Schema:
- ticket_id (TEXT)
- created_at (DATETIME)
- category (TEXT)
- priority (TEXT)
- status (TEXT)
- response_time_hrs (REAL)
- resolution_time_hrs (REAL)
- agent_id (TEXT)
- customer_rating (REAL)
- issue_summary (TEXT)

Critical Rules:
1. Use exact column names from the schema above (e.g., use `agent_id`, NOT `agent`).
2. Keep queries complete and non-truncated.
"""


def generate_sql(user_query: str):
  if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

  client = genai.Client(api_key=GEMINI_API_KEY)

  # Model name updated to an active supported model: gemini-3.6-flash
  response = client.models.generate_content(
      model="gemini-3.6-flash",
      contents=user_query,
      config=types.GenerateContentConfig(
          system_instruction=SYSTEM_PROMPT,
          temperature=0.0,
          max_output_tokens=300,
      ),
  )

  # Safely extract text parts without triggering 'thought_signature' warnings
  raw_text = ""
  if response.candidates and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
      if hasattr(part, "text") and part.text:
        raw_text += part.text

  # Clean SQL formatting output
  cleaned_sql = re.sub(r"```sql|```", "", raw_text).strip()

  return {
      "sql": cleaned_sql,
      "explanation": (
          f"Generated via Google Gemini 3.6 Flash for query: '{user_query}'"
      ),
  }