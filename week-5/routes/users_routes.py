from fastapi import APIRouter
from db_config import Session
from models import User
from schemas import UserCreate, UserLogin
from sqlalchemy import select
from datetime import datetime
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

pwd_scheme=os.getenv("PASSWORD_HASHING_SCHEME").split(",")



pwd_context = CryptContext(schemes=pwd_scheme, deprecated="auto")

users_router = APIRouter(tags=["Users"])

@users_router.get("")
def get_all_users(term:str=None):
    db=Session()
    query =select(User)
    users=db.execute(query).scalars().all()
    return users


@users_router.get("/{user_id}")
def get_user_by_id(user_id:int):
    db=Session()
    query =select(User).where(User.id==user_id)
    user=db.execute(query).scalar_one_or_none()
    return user


@users_router.post("")
def create_new_user(body:UserCreate):
    db=Session()
    query=select(User).where(User.email==body.email)
    user_exists = db.execute(query).scalar_one_or_none()

    if user_exists:
        return {"message":"User already exists","status_code":400,"success":False}
    new_user = User(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        age=body.age,
        password=pwd_context.hash(body.password),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created successfully","data":new_user,"status_code":201,"success":True}

@users_router.post("/login")
def user_login(body:UserLogin):
    db=Session()
    query =select(User).where(User.email==body.email)
    user=db.execute(query).scalar_one_or_none()

    if not user:
        return {"message":"Invalid credentials","status_code":401,"success":False}

    if not pwd_context.verify(body.password,user.password):
        return {"message":"Invalid credentials","status_code":401,"success":False}
    return {"message":"Login successful","data":user,"status_code":200,"success":True}   
    

@users_router.delete("/{user_id}")
def delete_user_by_id(user_id:int):
    for user in users:
        if user["user_id"] == user_id:
            users.remove(user)
            return f"User with the id {user_id} has been deleted successfully."
    return f"No user with the id {user_id} was not found."
    
@users_router.put("/{user_id}")
def update_user_by_id(user_id:int,body:dict):
    for user in users:
        if user["user_id"] == user_id:
            user.update(body)
            return f"User with the id {user_id} has been updated successfully."
    return f"No user with the id {user_id} was not found."

    # SQLAlchemy ORM
