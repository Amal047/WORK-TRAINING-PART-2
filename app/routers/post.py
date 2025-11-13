from fastapi import Response,status,HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter( prefix="/posts", tags=["Posts"])

# get all posts
@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    try:
        # cursor.execute("""SELECT * FROM post""")
        # posts = cursor.fetchall()
        posts = db.query(models.Post).all()
        return  posts
    except Exception as error:
        # conn.rollback()  
        raise HTTPException(status_code=500, detail=str(error))


# Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        # cursor.execute(
        #     """INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        #     (post.title, post.content, post.published)
        # )
        # new_post = cursor.fetchone()
        # conn.commit()

        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    
    except Exception as e:
        # conn.rollback()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
#get induvidual post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found"
        )
    
    return post
    
        

#deleating a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (id,)) 
    # can also use str(id) but not necassary doing this in other contexts could cause
    #  type mismatch issues later (especially with strict constraints).
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#updating a post   
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

     # cursor.execute( """ UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
     #     (post.title, post.content, post.published, id))
     # can also use str(id) but not necassary doing this in other contexts could cause
     # type mismatch issues later (especially with strict constraints).
     # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    
    # conn.commit()

    post_query.update(post_update.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
