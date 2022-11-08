import datetime
import logging
from time import time
from typing import Optional
from fastapi import HTTPException, status, Depends, BackgroundTasks, UploadFile
from fastapi.responses import JSONResponse

from core import settings
from core.connections import auth_db
# from app.core.image_handler import upload_image
# from app.jobs.stripe import delete_customer
from models import ResetPassword
from models.auth import PatchUser, User, CreateUser
# from app.models.stripe import StripeCustomer
from jobs.auth import create_access_token, get_password_hash
# from app.core.mail_handler import send_reset_alert_email, send_verification_email, send_reset_email

from jose import JWTError, jwt


logger = logging.getLogger(__name__)


async def grab_user(uuid: str) -> Optional[User]:
    try:
        user = auth_db.get_user(uuid)
        
        if not user:
            return
        
        return user

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching user.")


# async def create_user(request: CreateUser, background_tasks: BackgroundTasks):
#     try:
#         statement = select(User).where(User.email == request.email)
#         results = await session.execute(statement)
        
#         user = results.scalars().first()
    
#         if user:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email: {request.email} already exists.")
        
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
#     try:
#         new_user = User(
#             username=request.username,
#             full_name=request.full_name,
#             email=request.email,
#             hashed_password=get_password_hash(request.password),
#         )
        
        
#         session.add(new_user)    
#         await session.commit()
#         await session.refresh(new_user)
        
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating user.")
    
#     verify_token = create_access_token(new_user.uuid, datetime.timedelta(minutes=15))
    
#     logger.info(f"User {new_user.uuid} created. Sending verification email. Verify token: {verify_token.access_token}")
    
#     # background_tasks.add_task(send_verification_email, new_user.email, verify_token.access_token)
    
#     return new_user


# async def request_verify(email: str, background_tasks: BackgroundTasks):
#     try:
#         statement = select(User).where(User.email == email.lower())
#         results = await session.execute(statement)
        
#         user = results.scalars().first()
    
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found.")
        
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
        
#     verify_token = create_access_token(user.uuid, datetime.timedelta(minutes=15))
    
#     logger.info(f"User {user.uuid} requested verification email. Verify token: {verify_token.access_token}")
    
#     # background_tasks.add_task(send_verification_email, user.email, verify_token.access_token)
    
#     return {"message": "Verification email sent."}


async def request_reset(email: str, background_tasks: BackgroundTasks):
    try:
        statement = select(User).where(User.email == email.lower())
        results = await session.execute(statement)
        
        user = results.scalars().first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found.")
        
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
    
    reset_token = create_access_token(user.uuid, datetime.timedelta(minutes=15))
    
    logger.info(f"User {user.uuid} requested reset email. Verify token: {reset_token.access_token}")
    
    # background_tasks.add_task(send_reset_email, user.email, reset_token.access_token)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Verification email sent."})
    
    
async def reset_user_password(request: ResetPassword, background_tasks: BackgroundTasks):
    
    cred_except = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")
    
    try:
        payload = jwt.decode(request.token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        
        uuid: str = payload.get("uuid")
        exp: time = payload.get("exp")
    
        if uuid is None:
            raise cred_except
        
        if float(exp) <= time():
            raise cred_except
        
    except JWTError:
        raise cred_except
    
    try:
        statement = select(User).where(User.uuid == uuid)
        results = await session.execute(statement)
        
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
    user = results.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    
    user.hashed_password = get_password_hash(request.password)
    
    session.add(user)
    await session.commit()
    
    # background_tasks.add_task(send_reset_alert_email, user.email)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Password reset."})
    

# async def verify_user_email(token: str):
    
#     cred_except = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")
    
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        
#         uuid: str = payload.get("uuid")
#         exp: time = payload.get("exp")
    
#         if uuid is None:
#             raise cred_except
        
#         if float(exp) <= time():
#             raise cred_except
        
#     except JWTError:
#         raise cred_except
    
#     try:
#         statement = select(User).where(User.uuid == uuid)
#         results = await session.execute(statement)
        
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
#     user = results.scalars().first()
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    
#     user.is_verified = True
    
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)
    
#     return user
    
    
# async def get_all_users(limit: int = 100, last: str = None):
    
#     try:
       
#         users = auth_db.fetch(limit=limit, last=last)
        
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
#     return users


# async def get_user_by_uuid(uuid: str):
    
#     try:
#         statement = select(User).where(User.uuid == uuid)
#         results = await session.execute(statement)
        
#         user = results.scalars().first()
        
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    
#     return user


# async def patch_user_by_uuid(uuid: str, user_patch: PatchUser, current_user: User):
    
#     if not current_user.is_superuser:
#         if not current_user.uuid == uuid:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to edit this user.")
    
#     try:
#         statement = select(User).where(User.uuid == uuid)
#         results = await session.execute(statement)
        
#         user = results.scalars().first()
        
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with uuid: {uuid} not found.")
        
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
#     user.name = user_patch.name or user.name
    
#     user.email = user_patch.email or user.email
    
#     if user.is_superuser:
#         if not current_user.uuid == uuid:
    
#             user.is_superuser = user_patch.is_superuser or user.is_superuser
#             user.is_verified = user_patch.is_verified or user.is_verified
            
#             user.account_type = user_patch.account_type or user.account_type
            
            
#     user.updated_at = datetime.datetime.utcnow()
    
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)
    
#     return user


# async def delete_user_by_uuid(uuid: str, current_user: User):
#     try:
#         statement = select(User).where(User.uuid == uuid)
#         results = await session.execute(statement)
        
#         user = results.scalars().first()
        
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with uuid: {uuid} not found.")
        
#     except SQLAlchemyError as e:
#         logger.exception(e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error connecting to database.")
    
#     # try:
#     #     await delete_customer(user.stripe_account, session)
        
#     # except Exception as e:
#     #     logger.exception(e)
    
    
#     if not current_user.is_superuser:
#         if not current_user.uuid == user.uuid:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this user.")
    
#     await session.delete(user)
#     await session.commit()
    
#     return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User deleted."})


# async def upload_profile_image(file: UploadFile, user: User):
    
    
#     public_id = f"USER_{user.uuid}"
        
#     url = upload_image(file.file, public_id, "users")
    
#     user.picture = url
    
#     try:
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#     except SQLAlchemyError as e:
#         logger.exception(e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to store image path")