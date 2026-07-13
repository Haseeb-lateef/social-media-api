from .. import models, schemas, utility
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/",  status_code= status.HTTP_201_CREATED)
def vote(vote_data: schemas.VoteData, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    exist = db.query(models.Votes).filter(models.Post.id == vote_data.post_id).first()

    if not exist:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")



    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote_data.post_id, models.Votes.user_id == current_user.id)

    found_vote = vote_query.first()

    if vote_data.vote_dir == 1:

        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"the user {current_user.id} has already liked post {vote_data.post_id}")

        new_vote = models.Votes(post_id=  vote_data.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "liked post"}
    else:

        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "unliked post"}




        
       