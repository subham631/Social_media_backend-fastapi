from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) #unpack the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: str, db: Session = Depends(get_db)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"the post with id {id} not found")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (id))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User")


    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: str, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *""", (post.title, post.content, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post
