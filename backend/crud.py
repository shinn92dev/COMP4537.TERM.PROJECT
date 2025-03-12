from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, APIKey
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class DBController:
    def __init__(self):
        pass

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def insert_new_user(self, email, username, password, is_admin):
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

    def insert_data(self, table, **data):
        db: Session = SessionLocal()
        try:
            new_record = table(**data)
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            message = (
                f"✅ New data inserted successfully into {table.__tablename__}."
            )
            print(message)
            return {
                "success": True,
                "data": new_record,
                "message": message
                }
        except IntegrityError as e:
            db.rollback()
            return {
                "success": False,
                "error": "IntegrityError",
                "message": str(e)
                }
        except Exception as e:
            db.rollback()
            return {
                "success": False, 
                "error": "Exception", 
                "message": str(e)
                }
        finally:
            db.close()
    
    def select_all_user(self):
        db: Session = SessionLocal() 
        try:
            users = db.query(User).all()
            return users
        except Exception as e:
            print(f"⚠️ Data select failed: {e}")
        finally:
            db.close()

    def is_key_already_exist(self, new_key):
        db: Session = SessionLocal()
        try:
            existing_key = db.query(APIKey).filter(APIKey.key == new_key)
            if not existing_key:
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Could not check api key list: {e}")
        finally:
            db.close()

    def get_user_id_from_email(email: str):
        db: Session = SessionLocal()
        try:
            stmt = select(User).where(User.email == email)
            user = db.scalars(stmt).first()
            if not user:
                print(f"⚠No user found with email: {email}")
                return None
            return user.id
        except Exception as e:
            print(f"❌Error during finding user id by email: {e}")
            return None
        finally:
            db.close()


d = DBController()
print(d.insert_data(APIKey, id=1, key="qwert"))