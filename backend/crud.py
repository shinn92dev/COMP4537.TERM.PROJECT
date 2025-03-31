from sqlalchemy.orm import Session
from database import SessionLocal
from models import HTTPMethodEnum, User, APIKey, APIUsage
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

    def is_valid_api_key(self, api_key: str):
        db = SessionLocal()
        try:
            return (
                db.query(APIKey)
                .filter(APIKey.key == api_key).first() is not None
            )
        finally:
            db.close()

    def delete_api_key(self, user_id: int, api_key: str):
        db = SessionLocal()
        try:
            matching = db.query(APIKey).filter(
                APIKey.user_id == user_id, APIKey.key == api_key
                ).first()

            if matching:
                db.query(APIUsage).filter(APIUsage.key_id == matching.key_id).delete()
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

    def get_all_api_keys_for_a_user(self, user_id: int):
        db = SessionLocal()
        try:
            keys = db.query(APIKey).filter(APIKey.user_id == user_id).all()
            return keys if keys else None
        finally:
            db.close()
    def update_api_key_activation(self, api_key, update_status_to):
        db = SessionLocal()
        try:
            locate_the_key = db.query(APIKey).filter(APIKey.key == api_key).first()
            if locate_the_key:
                locate_the_key.active = update_status_to
                db.commit()
                return {
                "success": True,
                "message": "API key status updated successfully."
            }
            else:
                return {
                    "success": False,
                    "message": "API Key not found for the provided key."
                }
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }
        finally:
            db.close()

    def get_api_key_id_by_key(self, key: str):
        db = SessionLocal()
        try:
            locate_the_key = db.query(APIKey).filter(APIKey.key == key).first()
            if locate_the_key:
                return locate_the_key.key_id if locate_the_key else None
        except SQLAlchemyError as e:
            db.rollback()
        finally:
            db.close()

    def increase_api_usage_count(api_key: str, method: str, endpoint: str):
        db = SessionLocal()
        try:
            key = db.query(APIKey).filter(APIKey.key == api_key).first()
            if not key:
                return {"success": False, "message": "API Key not found."}

            method_enum = HTTPMethodEnum[method.upper()]

            usage = db.query(APIUsage).filter_by(
                key_id=key.key_id,
                method=method_enum,
                endpoint=endpoint
            ).first()

            if usage:
                usage.count += 1
            else:
                usage = APIUsage(
                    key_id=key.key_id,
                    method=method_enum,
                    endpoint=endpoint,
                    count=1
                )
                db.add(usage)

            db.commit()
            return {"success": True, "message": "API usage count updated."}

        except SQLAlchemyError as e:
            db.rollback()
            return {"success": False, "message": f"Database error: {str(e)}"}

        finally:
            db.close()

    def get_all_api_keys() -> list[str]:
        db = SessionLocal()
        try:
            keys = db.query(APIKey.key).all()
            return [k[0] for k in keys]
        finally:
            db.close()