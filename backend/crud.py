from sqlalchemy.orm import Session
from database import SessionLocal
from models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_new_user(email, name, password):
    db: Session = SessionLocal()
    try:
        new_user = User(
            email=email, name=name, password=password
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
