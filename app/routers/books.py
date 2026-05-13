"""Simple in-memory book store - keeps the app self-contained for k8s demos."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/books", tags=["books"])

_store: dict[int, dict] = {}
_counter = 0


class BookIn(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)


class BookOut(BookIn):
    id: int


@router.get("", response_model=list[BookOut])
def list_books():
    return list(_store.values())


@router.post("", response_model=BookOut, status_code=201)
def create_book(book: BookIn):
    global _counter
    _counter += 1
    record = {"id": _counter, **book.model_dump()}
    _store[_counter] = record
    return record


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    if book_id not in _store:
        raise HTTPException(status_code=404, detail="Book not found")
    return _store[book_id]


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in _store:
        raise HTTPException(status_code=404, detail="Book not found")
    del _store[book_id]
