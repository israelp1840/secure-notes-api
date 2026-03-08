from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import User, Note
from .schemas import NoteCreate, NoteOut
from .security import decode_token, encrypt_note, decrypt_note

router = APIRouter(prefix="/notes", tags=["notes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = authorization.split(" ", 1)[1].strip()
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return user


@router.post("", response_model=NoteOut)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = Note(owner_id=user.id, title=payload.title, ciphertext=encrypt_note(payload.body))
    db.add(note)
    db.commit()
    db.refresh(note)
    return NoteOut(id=note.id, title=note.title, body=payload.body)


@router.get("", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    notes = db.query(Note).filter(Note.owner_id == user.id).all()
    out: list[NoteOut] = []
    for n in notes:
        out.append(NoteOut(id=n.id, title=n.title, body=decrypt_note(n.ciphertext)))
    return out


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.owner_id == user.id, Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(note)
    db.commit()