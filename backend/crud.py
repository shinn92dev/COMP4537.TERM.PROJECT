from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, APIKey
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import UserInDB
import logging

logger = logging.getLogger(__name__)


class DBController:
    def __init__(self):
        pass

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def insert_data(self, table, **data):
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
            return None
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
            return user.user_id
        except Exception as e:
            print(f"❌Error during finding user id by email: {e}")
            return None
        finally:
            db.close()

    def get_api_key_by_user_id(self, user_id):
        db = SessionLocal()
        try:
            key = db.query(APIKey).filter(APIKey.user_id == user_id).first()
            return key.key if key else None
        finally:
            db.close()

    def is_valid_api_key(api_key: str):
        db = SessionLocal()
        try:
            return (
                db.query(APIKey)
                .filter(APIKey.key == api_key).first() is not None
            )
        finally:
            db.close()

    def delete_api_key(user_id: int, api_key: str):
        db = SessionLocal()
        try:
            matching = db.query(APIKey).filter(
                APIKey.user_id == user_id, APIKey.key == api_key
                ).first()

            if matching:
                db.delete(matching)
                db.commit()
                return True
            return False
        finally:
            db.close()

    def fetch_user_by_email(email: str):
        with SessionLocal() as db:
            try:
                statement = select(User).where(User.email == email)
                user = db.scalars(statement).first()
                if not user:
                    logger.warning(f"⚠No user found with email: {email}")
                    return None
                return UserInDB(**user.__dict__)

            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                return None

            except Exception as e:
                logger.error(f"❌Unexpected server error: {e}")
                return None

    def fetch_user_by_user_id(user_id: int):
        with SessionLocal() as db:
            try:
                statement = select(User).where(User.user_id == user_id)
                user = db.scalars(statement).first()
                if not user:
                    logger.warning(f"⚠No user found with user id: {user_id}")
                    return None
                return UserInDB(**user.__dict__)
            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                return None
            except Exception as e:
                logger.error(f"❌Unexpected server error: {e}")
                return None

    def get_api_key_id_by_user_id(self, user_id: int):
        db = SessionLocal()
        try:
            key = db.query(APIKey).filter(APIKey.user_id == user_id).first()
            return key.key_id if key else None
        finally:
            db.close()