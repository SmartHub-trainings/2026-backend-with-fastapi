from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_all_users():
    return "Welcome to fastapi."
