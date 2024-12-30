from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # For grouping in documentation -> url/docs
)
#---------------------------------------Getting all posts-----------------------------------------
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # query parameters: ?  &   %20 -> space in url
    # 'limit' query parameter gives user option to limit num search result -> ?limit= 
    # 'skip' query parameter gives user option to skip the first few -> skip=   -> ?limit= &skip=
    # 'search' query parameter gives user search option -> ?search= 

    # SQL version
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall() # fetching data from database
    #print(limit)
    # Python version
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # code for returning posts with their num likes
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts 
#-------------------------------------Creating a new post-------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # 201 for creating a post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)): # use Post skimma
    # SQL version
    #inserting new post into fastapi database
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published)) # This way is safe for SQL injectioin (Sanatizing)
    # new_post = cursor.fetchone()
    # conn.commit() #commit our changes in database or push it

    #Python version
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # Efficient version, good for table's with many fields
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#----------------------------------Get an individual post----------------------------------------------
#@router.get("/{id}", response_model=schemas.Post) 
@router.get("/{id}", response_model=schemas.PostOut) 
def get_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # SQL version
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post= cursor.fetchone() 

    #Python version
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

#-----------------------------------Deleting a post-------------------------------------------
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # SQL version
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #Python version
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perfom requested action")

    # For python
    db.delete(post_query)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#--------------------------------------Updating a post----------------------------------------
# for 'put' we need to pass all the content even if we only update a part of it
@router.put("/{id}", response_model=schemas.Post) 
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # SQL version
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # Python version
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perfom requested action")
    
    # Python
    post_query.update(updated_post.dict())
    db.commit()

    return post.first()


# url/docs -> show the automatically generated documentation for the API 
