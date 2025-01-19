import models, Oauth2
from fastapi import status,HTTPException,Depends, APIRouter
from schemas import Vote
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int  = Depends(Oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post does not exist!!")
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id==current_user.id)
    found_vote = vote_query.first()
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully deleted vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"mesage": "successfully deleted vote!!!"}
    
