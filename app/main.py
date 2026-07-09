import time


from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utility
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()





# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database= 'fastapi',user='postgres', password='aishat123@', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection successful")
#         break

#     except Exception as error:
#         print(f"Connection failed:{error}")
#         time.sleep(2)







# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()

#     return {"data": posts}


# def find_post(id: int)-> dict:

#     for post in my_posts:

#         if post["id"] == id:
#             return post
    
        

        
# @app.get("/")
# def root():
#     return {"message":"Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)







