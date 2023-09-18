from datetime import datetime

import starlette.status as status
from fastapi import APIRouter, Depends, Form, Request, responses
from fastapi.responses import RedirectResponse

from database import get_session
from models import Board, Note
from settings import TEMPLATES

router = APIRouter()


@router.get("/{note_id}")
def get_note(request: Request, note_id: int, db=Depends(get_session)):
    note = db.query(Note).get(note_id)
    return TEMPLATES.TemplateResponse("note.html", {"request": request, "note": note})


@router.get("/add/")
def add_note_html(request: Request, db=Depends(get_session)):
    board = db.query(Board).all()
    return TEMPLATES.TemplateResponse("add.html", {"request": request, "boards": board})


@router.post("/add/")
def add_note(content: str = Form(default=""), board: int = Form(default=""), db=Depends(get_session)):
    new_note = Note(content=content, board_id=board)
    db.add(new_note)
    db.commit()
    return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/edit/{note_id}")
def edit_html(note_id: int, request: Request, db=Depends(get_session)):
    note = db.query(Note).get(note_id)
    return TEMPLATES.TemplateResponse("edit.html", {"request": request, "note": note})


@router.post("/edit/{note_id}")
def edit_note(note_id: int, content: str = Form(default=""), db=Depends(get_session)):
    note = db.query(Note).get(note_id)
    note.content = content
    note.change_time = datetime.now().strftime("%m.%d.%Y, %H:%M:%S")
    db.commit()
    db.close()
    return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{note_id}")
def delete_note(note_id: int, db=Depends(get_session)):
    note = db.query(Note).get(note_id)
    db.delete(note)
    db.commit()
    return RedirectResponse("/")
