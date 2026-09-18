import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import init_db, execute_query
from llm_engine import generate_sql
from anomaly_engine import detect_anomalies


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initializes SQLite database on API startup
    init_db()
    yield


app = FastAPI(title="AI Support Agent API", lifespan=lifespan)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"status": "API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "System operational"}


@app.post("/query")
def process_query(req: QueryRequest):
    try:
        # Step 1: Generate SQL via LLM
        llm_res = generate_sql(req.query)
        print(f"\n[DEBUG] Generated SQL:\n{llm_res['sql']}\n")

        # Step 2: Execute SQL on database
        data, error = execute_query(llm_res["sql"])
        if error:
            print(f"[DEBUG] SQLite Error: {error}")
            raise HTTPException(status_code=400, detail=f"Database execution error: {error}")

        return {
            "sql_generated": llm_res["sql"],
            "explanation": llm_res["explanation"],
            "result": data,
        }

    except HTTPException:
        raise
    except Exception as e:
        # Print full trace to Uvicorn terminal for debugging
        print("\n================ ERROR IN /query ================")
        traceback.print_exc()
        print("=================================================\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/anomalies")
def get_anomalies():
    try:
        return {"anomalies": detect_anomalies()}
    except Exception as e:
        print(f"[DEBUG] Anomaly detection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))