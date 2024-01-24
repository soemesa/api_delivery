from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import UserSchema, Message
from src.security import get_password_hash, get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=Message, status_code=201)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(User.username == user.username))
    if db_user:
        raise HTTPException(status_code=400, detail='Usuário já registrado!')

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, email=user.email, password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return Message(message='Usuário registrado com sucesso!')


@router.get('/', response_model=None, status_code=200)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User). offset(skip).limit(limit)).all()

    return {'users': users}


@router.put('/{user_id}', response_model=Message, status_code=200)
def update_user(user_id: int, user: UserSchema, session: Session, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail='Usuário não autorizado!')

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return Message(message='Usuário atualizado com sucesso!')


@router.delete('/{user_id}', response_model=Message, status_code=200)
def delete_user(user_id: int, session: Session, current_user: CurrentUser):

    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail='Usuário não autorizado!')

    session.delete(current_user)
    session.commit()

    return Message(message='Usuário apagado com sucesso!')



