from fastapi import FastAPI 
from . import models 
from .database import engine 
from.routers import post, user, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#router inclusion
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# path operation
@app.get("/") #decorator

#a asyinc function
async def root():
    return { "Message": "Hello World"}


#------------------------------------------------------------------------------#
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

