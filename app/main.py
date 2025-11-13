from fastapi import FastAPI #,Response,status,HTTPException, Depends
from . import models #, schemas, utils
from .database import engine #, get_db
# from fastapi.params import Body
# from typing import Optional,List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
from.routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#router inclusion
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i


# def find_post(id):
#     for p in my_posts:
#         if p["id"]  == id:
#             return p

