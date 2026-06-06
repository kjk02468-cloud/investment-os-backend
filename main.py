"""
Investment OS — FastAPI server.
The dark dashboard's fetch points here. The Anthropic key never reaches the browser.

Run locally:   uvicorn main:app --reload --port 8000
Endpoints:
  GET  /health
  POST /api/agent           {"task": "..."} or {"key": "brief"|"hbm"|..., "evaluate": false}
  GET  /api/thesis/{ticker} runs 6-condition health-check, alerts Telegram on RISK
  POST /api/brief           full daily brief + Telegram push
"""
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import agent

app = FastAPI(title="Investment OS Agent", version="1.0")

# CORS — set ALLOWED_ORIGINS to your dashboard host(s), comma-separated.
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class AgentReq(BaseModel):
    task: Optional[str] = None
    key: Optional[str] = None
    evaluate: bool = False


@app.get("/health")
def health():
    return {"ok": True, "model": agent.MODEL, "search_tool": agent.WEB_SEARCH_TOOL}


@app.post("/api/agent")
def api_agent(req: AgentReq):
    task = req.task or agent.TASKS.get(req.key or "")
    if not task:
        raise HTTPException(status_code=400, detail="`task` or a valid `key` is required")
    try:
        return agent.run_agent(task, evaluate=req.evaluate)
    except Exception as e:  # noqa
        raise HTTPException(status_code=502, detail=f"agent error: {e}")


@app.get("/api/thesis/{ticker}")
def api_thesis(ticker: str):
    try:
        return agent.thesis_check(ticker)
    except Exception as e:  # noqa
        raise HTTPException(status_code=502, detail=f"thesis error: {e}")


@app.post("/api/brief")
def api_brief():
    try:
        return agent.daily_brief(notify=True)
    except Exception as e:  # noqa
        raise HTTPException(status_code=502, detail=f"brief error: {e}")
