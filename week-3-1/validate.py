from pydantic import BaseModel,Field,model_validator

class UserCreate(BaseModel):
    first_name:str
    last_name:str
    other_name:str|None=None
    age:int
    password:str=Field(...,min_length=8)
    confirmPassword:str

    @model_validator(mode="after")
    def confirm_password(self):
        if self.password != self.confirmPassword:
            raise ValueError("Passwords do not match.")

        return self
