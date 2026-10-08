

def serialize_user(raw_user):
    return {"id":raw_user[0], 
        "first_name":raw_user[1], 
        "last_name":raw_user[2], 
        "email":raw_user[3], 
        "age":raw_user[4], 
        "created_at":raw_user[6], 
        "updated_at":raw_user[7], 
        "is_verified":bool(raw_user[8])}