
from fastapi import Depends, APIRouter, status, HTTPException
from h11 import Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=['votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def voting(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id==current_user.id, models.Vote.post_id==vote.post_id)

    vote_found = vote_query.first()

    if vote.vote_dir == 0:
        if vote_found==None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User of id {current_user.id} Not voted post of id {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
    
    if vote.vote_dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User of id {current_user.id} Already voted this post of id {vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    
