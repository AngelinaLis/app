from datetime import datetime

import starlette.status as status
import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Form, Request, responses
from fastapi.responses import RedirectResponse

from database import get_session
from models import Board, Note
from routers import boards, notes
from settings import TEMPLATES

app = FastAPI()
app.include_router(boards.router, prefix="/board")
app.include_router(notes.router, prefix="/note")


@app.get("/")
def index(request: Request, db=Depends(get_session)):
    notes = db.query(Note).all()
    boards = db.query(Board).all()
    return TEMPLATES.TemplateResponse("index.html", {"request": request, "notes": notes, "boards": boards})


if __name__ == "__main__":
    uvicorn.run(app, port=8100, host="0.0.0.0")
