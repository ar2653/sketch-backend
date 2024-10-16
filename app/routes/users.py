from fastapi import APIRouter, HTTPException
from botocore.exceptions import ClientError
from app.models.user import User, UserCredentials
from app.db import pb
import bcrypt
from pocketbase.utils import ClientResponseError

router = APIRouter()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/")
async def create_user(user: User):
    try:
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        pb.collection('members').create(user.model_dump())
        return {"message": "User created successfully"}
    except ClientError as e:
        print(f"Couldn't create user: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user in PocketBase")
    except ClientResponseError as e:
        print(f"PocketBase error: {e}")
        if e.status == 400:
            raise HTTPException(status_code=400, detail=f"Invalid user data: {e.data}")
        raise HTTPException(status_code=500, detail="Failed to create user in PocketBase")
    
@router.post("/login")
async def login_user(credentials: UserCredentials):
    try:
        response = pb.collection('members').get_list(1, 1, {
            'filter': f'email="{credentials.email}"'
        })
        if response.items:
            user = response.items[0]
            if verify_password(credentials.password, user.password):
                return {"message": "Login successful", "user": user}
            else:
                raise HTTPException(status_code=401, detail="Invalid password")
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(f"Error occurred during login: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user from PocketBase")
