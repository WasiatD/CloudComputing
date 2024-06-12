from firebaseconfig import pyrebaseauth,auth
from fastapi import HTTPException


def login_user(email, password):
    try:
        user = pyrebaseauth.sign_in_with_email_and_password(email, password)
        # user = auth.get_user_by_email(email)
        # custom_token = auth.create_custom_token(user.uid)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def register_user(email, password):
    try:
        user = pyrebaseauth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def validate_token(token: str):
    try:
        # Verify the token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_current_user_id(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        raise e

def get_current_user_by_email(email):
    try:
        user = auth.get_user_by_email(email)
        uid = user.uid
        return uid
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))