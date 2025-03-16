import bcrypt
from crud import DBController
from models import User


def hash_password(password: str) -> str:
    encoded_password = password.encode()
    salt_round = 10
    salt = bcrypt.gensalt(salt_round)
    return bcrypt.hashpw(encoded_password, salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    encoded_password = password.encode()
    encoded_hashed_password = hashed_password.encode()
    return bcrypt.checkpw(encoded_password, encoded_hashed_password)


def authenticate_user(email: str, password: str):
    user = DBController.fetch_user_by_email(email)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def main():
    print("Starting auth.py main function...")
    
    # Try to authenticate the admin user
    print("Trying to authenticate admin user...")
    user = authenticate_user("admin@admin.ca", "admin")
    if user:
        print(f"Authentication successful: {user}")
    else:
        print("Authentication failed, creating admin user...")
        
        # Create admin user
        test_user = {
            "email": "admin@admin.ca",
            "username": "admin",
            "password": hash_password("admin"),
            "is_admin": True
        }
        
        print(f"Admin user data: {test_user}")
        
        db = DBController()
        result = db.insert_data(User, **test_user)
        print(f"Insert result: {result}")
    
    print("Auth.py main function completed.")


if __name__ == '__main__':
    main()
