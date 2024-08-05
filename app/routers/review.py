
from app import oauth2
from .. import models, schemas, oauth2
from typing import List
from fastapi import Body, FastAPI, Query, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]  # tag for swagger
)

# getting all reviews
@router.get("/", response_model=List[schemas.Review])
def get_reviews(db: Session = Depends(get_db), rating: int = Query(None, ge=1, le=5)):
    # cursor.execute("""SELECT * FROM reviews """)
    # reviews = cursor.fetchall()
    if rating is not None:
        reviews = db.query(models.Review).filter(models.Review.rating == rating).all()
        if reviews == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'No reviews found with rating {rating}')
    else:
        reviews = db.query(models.Review).all()
    
    return reviews

# create a review // 201 http status code = create
# get_current_user: int = Depends(oauth2.get_current_user)  + user_id: int = Depends(oauth2.get_current_user)-> user must be logged in to create review
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db), 
                  get_current_user: int = Depends(oauth2.get_current_user),
                  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO reviews (user_id, content, rating) VALUES (%s, %s, %s)
    #               RETURNING * """, 
    #               (review.user_id, review.content, review.rating))
    # new_review = cursor.fetchone()

    # conn.commit()   # saving all

    # verify if current user has already posted an review
    existing_review = db.query(models.Review).filter(models.Review.user_id == current_user.id).first()
    if existing_review:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already posted a review")
    

    #unpack the review /// user_id=current_user.id -> assign the id to the user_id from review
    new_review = models.Review(user_id=current_user.id, **review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)  # retrive and sotre in new review

    return new_review

# getting 1 review -  response: Response, 
@router.get("/{id}", response_model=schemas.Review)
def get_review(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from reviews WHERE id = %s """,
    #               (str(id)))
    # review = cursor.fetchone()

    review = db.query(models.Review).filter(models.Review.id == id).first()

    # exception if the review was not found 
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'review with id {id} was not found')
    return review

# delete 1 review
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id:int, db: Session = Depends(get_db), 
                  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM reviews WHERE id = %s RETURNING * """,
    #              (str(id),))
    # del_review = cursor.fetchone()
    # conn.commit()
    del_review_query = db.query(models.Review).filter(models.Review.id == id)

    del_review = del_review_query.first()

    if del_review == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'review with id {id} was not found')
    
    # check if it's his review
    if del_review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perfom requested actions")

    del_review_query.delete(synchronize_session=False)
    db.commit()
    # used when you don't want to send data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Review)
def update_review(id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db), 
                  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE reviews SET user_id = %s, content = %s, rating = %s WHERE id = %s RETURNING *""",
    #               (review.user_id, review.content, review.rating, str(id)))
    # updated_review = cursor.fetchone()
    # conn.commit()
    update_review_query = db.query(models.Review).filter(models.Review.id == id)

    #ia primu
    up_review = update_review_query.first()

    #daca nu exista
    if up_review == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'review with id {id} was not found')
    
    # check if it's his review
    if up_review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perfom requested actions")

    
    # daca exista luam dictionaru cu toate mentionate de care avem nevoie
    update_review_query.update(review.dict(), synchronize_session=False)
    
    db.commit()
    return update_review_query.first()
