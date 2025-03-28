from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from crud import DBController
from schemas import TokenData
import logging

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"SECRET_KEY loaded: {'Yes' if SECRET_KEY else 'No'}")
logger.info(f"ALGORITHM: {ALGORITHM}")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

if not SECRET_KEY:
    raise ValueError(
        "SESSION_KEY is not set! Please configure it in .env "
        "or environment variables."
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    logger.info(f"Creating access token for data: {data}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    logger.info(f"Token will expire at: {expire.isoformat()}")
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token created successfully, first 20 chars: {encoded_jwt[:20]}...")
    return encoded_jwt


async def get_current_user(request: Request):
    logger.info("Attempting to get current user from request")
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logger.info(f"Cookies in request: {request.cookies}")
    
    token = request.cookies.get("access_token")
    if not token:
        logger.warning("No access_token found in cookies")
        raise credential_exception

    logger.info(f"Token found in cookies, first 20 chars: {token[:20]}...")

    try:
        logger.info("Attempting to decode token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Token decoded successfully: {payload}")
        
        user_id = int(payload.get("sub"))
        logger.info(f"User ID from token: {user_id}")
        
        if not user_id:
            logger.warning("No user_id found in token payload")
            raise credential_exception
            
        token_data = TokenData(user_id=user_id)
        logger.info(f"TokenData created: {token_data}")

    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except InvalidTokenError as e:
        logger.warning(f"Invalid token error: {str(e)}")
        raise credential_exception

    logger.info(f"Fetching user from database with ID: {token_data.user_id}")
    user = DBController.fetch_user_by_user_id(token_data.user_id)
    
    if not user:
        logger.warning(f"No user found with ID: {token_data.user_id}")
        raise credential_exception

    logger.info(f"User retrieved successfully: user_id={user.user_id}, is_admin={user.is_admin}")
    return user


async def check_is_admin(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "is_admin" not in payload:
            logger.info("is_admin key not found in token payload → returning None")
            return None
        is_admin = payload["is_admin"]
        
        return is_admin
    
    except (ExpiredSignatureError, InvalidTokenError):
        return None
    

async def get_current_user_id(request: Request):
    logger.info("Attempting to get current user from request")
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logger.info(f"Cookies in request: {request.cookies}")
    
    token = request.cookies.get("access_token")
    if not token:
        logger.warning("No access_token found in cookies")
        raise credential_exception

    logger.info(f"Token found in cookies, first 20 chars: {token[:20]}...")

    try:
        logger.info("Attempting to decode token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Token decoded successfully: {payload}")
        
        user_id = int(payload.get("sub"))
        logger.info(f"User ID from token: {user_id}")
        
        if not user_id:
            logger.warning("No user_id found in token payload")
            raise credential_exception
        
        return user_id
    
    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except InvalidTokenError as e:
        logger.warning(f"Invalid token error: {str(e)}")
        raise credential_exception
    

def main():
    pass


if __name__ == '__main__':
    main()