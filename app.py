from fastapi import Depends, FastAPI, Request

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
