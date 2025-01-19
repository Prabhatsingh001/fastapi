import models
from fastapi import Response,status,HTTPException,Depends,APIRouter
from schemas import Post,PostResponse
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import Oauth2
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get('/', response_model=List[PostResponse])
def open(db : Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user),limit: int=10, skip:int=0, search: Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset=skip).all()
    return {"message": posts}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: Post, db : Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}


@router.get("/{id}")
def get_post(id:int, db : Session = Depends(get_db), response_model = List[PostResponse], current_user: int = Depends(Oauth2.get_current_user)):
    test_post = db.query(models.Post).filter(models.Post.id==id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
    return {"data": test_post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    post = delete_post.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist") 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorised")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def upadte_post(id: int, post: Post, db : Session = Depends(get_db), response_model = PostResponse, current_user: int = Depends(Oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    if updated_post.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allowed")
    upadte_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": updated_post.first()}
