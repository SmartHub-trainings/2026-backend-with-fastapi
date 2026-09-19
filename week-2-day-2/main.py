from fastapi import FastAPI
app = FastAPI()

@app.get("/users")
def get_all_users():
    return [1,2,3]

@app.get("/users/{user_id}")
def get_user_by_id(user_id:int):
    return f"Getting information of user with id {user_id}"
