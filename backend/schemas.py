from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | str | None = None
    email: str | None = None
    is_admin: bool | None = None


class User(BaseModel):
    user_id: int | str
    email: str | None = None
    username: str | None = None
    is_admin: bool | None = None


class UserInDB(User):
    password: str


class UserDashboardResponse(BaseModel):
    username: str
    email: str
    request_limit: int
    remaining_requests: int


def main():
    pass


if __name__ == '__main__':
    main()
