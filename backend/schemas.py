from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class User(BaseModel):
    name: str
    email: str | None = None


class UserInDB(User):
    password: str




def main():
    pass


if __name__ == '__main__':
    main()
