from pydantic import BaseModel , EmailStr,Field,model_validator

class UserLogin(BaseModel):
    email:EmailStr
    password:str


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

