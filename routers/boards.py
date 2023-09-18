from datetime import datetime

import starlette.status as status
from fastapi import APIRouter, Depends, Form, Request, responses
from fastapi.responses import RedirectResponse

from database import get_session
from models import Board, Note
from settings import TEMPLATES

router = APIRouter()


@router.get("/{board_id}")
def get_board(request: Request, board_id: int, db=Depends(get_session)):
    board = db.query(Board).get(board_id)
    return TEMPLATES.TemplateResponse("board.html", {"request": request, "board": board})


@router.post("/{board_id}")
def board(board_id: int, new_name: str = Form(default=""), db=Depends(get_session)):
    board = db.query(Board).get(board_id)
    board.name = new_name
    board.change_time = datetime.now().strftime("%m.%d.%Y, %H:%M:%S")
    db.commit()
    db.close()
    return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.post("/add/")
def add_board(name: str = Form(default=""), db=Depends(get_session)):
    new_board = Board(name=name)
    db.add(new_board)
    db.commit()
    return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/add/")
def add_board_html(request: Request, db=Depends(get_session)):
    board = db.query(Board).all()
    return TEMPLATES.TemplateResponse("add_board.html", {"request": request, "board": board})
