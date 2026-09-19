from fastapi import FastAPI
app = FastAPI()
users =[
    {"first_name":"Daniel","last_name":"Tadesse","user_id":1},
    {"first_name":"Selinam","last_name":"Tosia","user_id":2},
    {"first_name":"Samrawit","last_name":"Zewdie","user_id":3},
    {"first_name":"Zerife","last_name":"Ahmed","user_id":4},
    {"first_name":"Lidiya","last_name":"Bekele","user_id":5},
    {"first_name":"Habtamu","last_name":"Assefa","user_id":6},
    {"first_name":"Natnael","last_name":"Kifle","user_id":7},
    {"first_name":"Girma","last_name":"Mulatu","user_id":8},
    {"first_name":"Muna","last_name":"Abdella","user_id":9},
    {"first_name":"Abebe","last_name":"Tola","user_id":10}
]

@app.get("/users")
def get_all_users(term:str=None):
    if term ==None:
        return users
    else:
        searched_users=[]
        for user in users:
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
def create_new_user(body:dict):
    # print(body)
    user =body
    user["user_id"] = len(users) +1
    users.append(user)
    return {"message":"User created successfully","data":user}
    