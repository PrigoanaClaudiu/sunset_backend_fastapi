from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(database.get_db),
                   current_user: Optional[models.User] = Depends(oauth2.get_current_user_optional)):
    
    reservation_data = reservation.dict()

    if reservation.data_start > reservation.data_finish:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data de început trebuie să fie înainte de data de sfârșit.")

    if current_user:
        reservation_data.update({"user_id": current_user.id, "name": current_user.name, "email": current_user.email})
    else:
        if not reservation_data.get("name") or not reservation_data.get("email"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Numele și email-ul sunt obligatorii pentru utilizatorii neautentificați.")

    new_reservation = models.Reservation(**reservation_data)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation