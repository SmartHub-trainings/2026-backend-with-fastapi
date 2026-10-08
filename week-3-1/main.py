from fastapi import FastAPI
from pydantic import BaseModel,Field,model_validator,EmailStr
import sqlite3
from passlib.context import CryptContext


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

conn=sqlite3.connect("mydb.db")
cur=conn.cursor()
# cur.execute("drop table users")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(20) NOT NULL UNIQUE,
    age INTEGER,
    password VARCHAR(60) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
)
""")

# all_users=cur.execute("select * from users").fetchall()
# print(all_users)




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
    conn=sqlite3.connect("mydb.db")
    cur=conn.cursor()
    users=cur.execute("select * from users").fetchall()
    mod_users=[]
    for user in users:
        mod_users.append(serialize_user(user))
    if term ==None:
        return mod_users
    else:
        searched_users=[]
        for user in mod_users:
            if user["first_name"].lower().startswith(term.lower()) or user["last_name"].lower().startswith(term.lower()):
                searched_users.append(user)
        return searched_users


@app.get("/users/{user_id}")
def get_user_by_id(user_id:int):
    for user in users:
        if user["user_id"] == user_id:
            return user
       
    return f"No user with the id {user_id} was found."


@app.post("/users")
def create_new_user(body:UserCreate):
    conn=sqlite3.connect("mydb.db")
    cur=conn.cursor()
    existing_user=cur.execute("select * from users where email =?",(body.email,)).fetchone()
    if existing_user:
        return {"message":"User already exists","status_code":400,"success":False}
    cur.execute("""
    INSERT INTO users (first_name,last_name,age,password,email)
    VALUES (?,?,?,?,?)
    """,(body.first_name,body.last_name,body.age,pwd_context.hash(body.password),body.email))
    conn.commit()
    
    raw_user = cur.execute("select * from users where email =?",(body.email,)).fetchone()
    conn.close()
    user=serialize_user(raw_user)   
    return {"message":"User created successfully","data":user,"status_code":201,"success":True}

@app.post("/users/login")
def user_login(body:UserLogin):
    conn=sqlite3.connect("mydb.db")
    cur=conn.cursor()
    user=cur.execute("select * from users where email =?",(body.email,)).fetchone()

    if not user:
        return {"message":"Invalid credentials","status_code":401,"success":False}

    if not pwd_context.verify(body.password,user[5]):
        return {"message":"Invalid credentials","status_code":401,"success":False}
    return {"message":"Login successful","data":serialize_user(user),"status_code":200,"success":True}   
    

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
