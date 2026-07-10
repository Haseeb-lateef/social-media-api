from .. import models, schemas, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)






@router.get("/", response_model= List[schemas.PostReponse])
def get_posts(db: Session = Depends(get_db), limit:int = 10, skip: int = 0 ):

    # cursor.execute("""SELECT * FROM posts ORDER BY id""")
    # posts = cursor.fetchall()
    # print(posts)
    print(limit)
    print(skip)
    posts = db.query(models.Post).order_by(models.Post.id).limit(limit).offset(skip).all()
   
    
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostReponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))

    # new_post = cursor.fetchone
    # conn.commit()


    

    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)





    return new_post

@router.get("/{id}",response_model= schemas.PostReponse)
def get_post(id: int, db: Session = Depends(get_db)):


    # cursor.execute("""SELECT * FROM posts where id = %s """,(str(id),))

    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=  f"post with {id} not found")
        

    return post




@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING *""",(str(id),))

    # post = cursor.fetchone()
    # conn.commit()   

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the post of id:{id} dose not exist")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorised to performrequested action")
    

    post_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model= schemas.PostReponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title =%s, content=%s WHERE id = %s RETURNING * """,(post.title,post.content,str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)


    updated_post = post_query.first()

    


    if not updated_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the post of id={id} dose not exist")
    

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")


    

    
    post_query.update(post.model_dump(), synchronize_session= False)

    db.commit()
    

    return post_query.first()