from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True # setting optional field and defalt value


# try:
#     conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user= 'postgres',
#                              password= '', cursor_factory= RealDictCursor)
#     cursor = conn.cursor()
#     print("Database Connection was successful")
# except Exception as error:
#     print("Connection to dtabase failed")
#     print("Error:", error)

# my_posts = [{"title": "post 1", "content": "content of post 1", "id": 1},
#             {"title": "post 2", "content": "content of post 2", "id": 2}]

# path operation
@app.get("/") #decorator

#a asyinc function
async def root():
    return { "Message": "Hello World"}

# @app.get("/post")
# #normal function 
# def get_post():
#     return {"data": "This is your post"}

# @app.post("/createpost")
# def create_post():
#     return {"post": "post created successfully"}

# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"Name: {payload["Name"]}  Desig:{payload["Desig"]}"}

# @app.post("/post")
# def create_post(post: Post):
#     print(post)
#     print(post.dict()) # converting pydantic model to dictionary
#     return {'data': post}


# get all posts
@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    try:
        # cursor.execute("""SELECT * FROM post""")
        # posts = cursor.fetchall()
        posts = db.query(models.Post).all()
        return {"data": posts}
    except Exception as error:
        # conn.rollback()  
        raise HTTPException(status_code=500, detail=str(error))


# Create post
@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
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
        return {"data": new_post}
    except Exception as e:
        # conn.rollback()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def find_post(id):
    for p in my_posts:
        if p["id"]  == id:
            return p
        
#get induvidual post
@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found"
        )
    
    return post
    

 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        

#deleating a post
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

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
@app.put("/post/{id}")
def update_post(id: int, updated_post = Post, db: Session = Depends(get_db)):

     # cursor.execute( """ UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
     #     (post.title, post.content, post.published, id))
     # can also use str(id) but not necassary doing this in other contexts could cause
     # type mismatch issues later (especially with strict constraints).
     # updated_post = cursor.fetchone()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    
    # conn.commit()
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post

