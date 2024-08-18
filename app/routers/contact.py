from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

# from app.utils import send_contact_email
from .. import models, schemas, database, oauth2
# from ..email_utils import send_contact_email


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db),
                   current_user: Optional[models.User] = Depends(oauth2.get_current_user_optional)):
    
    contact_data = contact.dict()
    
    if current_user:
        contact_data.update({"user_id": current_user.id, "name": current_user.name, "email": current_user.email})
    else:
        # Utilizatorii neautentificați trebuie să furnizeze aceste informații
        if not contact_data.get("name") or not contact_data.get("email"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name and email please!")
        
    new_contact = models.Contacts(**contact_data)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact