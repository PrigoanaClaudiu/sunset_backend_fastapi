from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, review, auth, contact, reservation
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine)  /// don't need it anymore bcs of alembic

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#review from ..router
app.include_router(review.router)

#user from ..router - rutele 
app.include_router(user.router)

# router for auth
app.include_router(auth.router)

# router for contact
app.include_router(contact.router)

# router for reservation
app.include_router(reservation.router)

# path opperation
@app.get("/")   #   decorator + "/path"
def root():
    return {"message": "w"}

