from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, APIKey
from sqlalchemy import select


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_new_user(email, username, password, is_admin):
    db: Session = SessionLocal()
    try:
        new_user = User(
            email=email, username=username, password=password, is_admin=is_admin
            )
        db.add(new_user)
        db.commit()
        print("✅ New user data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"⚠️ New user data insertion failed: {e}")
    finally:
        db.close()


def select_all_user():
    db: Session = SessionLocal() 
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        print(f"⚠️ Data select failed: {e}")
    finally:
        db.close()


def is_key_already_exist(new_key):
    db: Session = SessionLocal()
    try:
        existing_key = db.query(APIKey).filter()
        if not existing_key:
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Could not check api key list: {e}")
    finally:
        db.close()


def get_user_id_from_email(email: str):
    try:
        stmt = select(User).where(User.email == email)
        user = session.scalars(stmt).all()
        if len(user) > 1:
            return
        elif len(user) == 0:
            print(f"⚠No user found with email: {email}")
            return
        return user[0].id
    except Exception as e:
        print(f"❌Error during finding user id by email: {e}")


def insert_new_api_key(user_id, api_key):
    db: Session = SessionLocal()
    new_key = APIKey()


# insert_new_user("user@user.com", "user", "12345", False)
# insert_new_user("admin@admin.com", "admin", "12345", True)
print(get_user_id_from_email("user@user.com"))
print(get_user_id_from_email("admin@admin.com"))
print(get_user_id_from_email("admin@admin.comm"))
