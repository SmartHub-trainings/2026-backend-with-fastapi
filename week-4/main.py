from fastapi import FastAPI
from pydantic import BaseModel,Field,model_validator,EmailStr
from datetime import datetime
# import os
# os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"

from passlib.context import CryptContext
from sqlalchemy import create_engine, Integer, String, DateTime, Boolean, func,select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine("sqlite:///mydb.db", connect_args={"check_same_thread": False}, echo=True)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass






pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# print(pwd_context.hash("password"))
# print(pwd_context.hash("password"))
def serialize_user(raw_user):
    return {"id":raw_user[0], 
        "first_name":raw_user[1], 
        "last_name":raw_user[2], 
        "email":raw_user[3], 
        "age":raw_user[4], 
        "created_at":raw_user[6], 
        "updated_at":raw_user[7], 
        "is_verified":bool(raw_user[8])}

#

# class User(Base):
#     __tablename__="users"

#     id=Column(Integer,primary_key=True)
#     first_name=Column(String(20),nullable=False)
#     last_name=Column(String(20),nullable=False)
#     email=Column(String(20),nullable=False,unique=True)
#     age=Column(Integer)
#     password=Column(String(60),nullable=False)
#     created_at=Column(TIMESTAMP,default=func.now())
#     updated_at=Column(TIMESTAMP,default=func.now())
#     is_verified=Column(Boolean,default=False)

class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name:Mapped[str]=mapped_column(String(20),nullable=False)
    last_name:Mapped[str]=mapped_column(String(20),nullable=False)
    email:Mapped[str]=mapped_column(String(20),nullable=False,unique=True)
    age:Mapped[int]=mapped_column(Integer)
    password:Mapped[str]=mapped_column(String(60),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now)
    is_verified:Mapped[bool]=mapped_column(Boolean,default=False)

# all_users=cur.execute("select * from users").fetchall()
# print(all_users)

Base.metadata.create_all(engine)




class UserCreate(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    age:int =Field(...,ge=16)
    password:str=Field(...,min_length=8)
    confirmPassword:str

    @model_validator(mode="after")
    def confirm_password(self):
        if self.password != self.confirmPassword:
            raise ValueError("Passwords do not match.")

        return self

class UserLogin(BaseModel):
    email:EmailStr
    password:str


app = FastAPI()

@app.get("/users")
def get_all_users(term:str=None):
    db=Session()
    query =select(User)
    users=db.execute(query).scalars().all()
    return users


@app.get("/users/{user_id}")
def get_user_by_id(user_id:int):
    db=Session()
    query =select(User).where(User.id==user_id)
    user=db.execute(query).scalar_one_or_none()
    return user


@app.post("/users")
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

@app.post("/users/login")
def user_login(body:UserLogin):
    db=Session()
    query =select(User).where(User.email==body.email)
    user=db.execute(query).scalar_one_or_none()

    if not user:
        return {"message":"Invalid credentials","status_code":401,"success":False}

    if not pwd_context.verify(body.password,user.password):
        return {"message":"Invalid credentials","status_code":401,"success":False}
    return {"message":"Login successful","data":user,"status_code":200,"success":True}   
    

@app.delete("/users/{user_id}")
def delete_user_by_id(user_id:int):
    for user in users:
        if user["user_id"] == user_id:
            users.remove(user)
            return f"User with the id {user_id} has been deleted successfully."
    return f"No user with the id {user_id} was not found."
    
@app.put("/users/{user_id}")
def update_user_by_id(user_id:int,body:dict):
    for user in users:
        if user["user_id"] == user_id:
            user.update(body)
            return f"User with the id {user_id} has been updated successfully."
    return f"No user with the id {user_id} was not found."

    # SQLAlchemy ORM
