from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

# OAuth2PasswordRequestForm -> username + password
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify_pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #creating token - after user, i can put more details (i will see) 
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})   # id must be str

    
    return {"access_token": access_token, "token_type": "bearer", 
            "user_name": user.name, "user_email": user.email, "role": user.role}