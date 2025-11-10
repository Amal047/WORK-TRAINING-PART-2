from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    Remote: bool = True # setting optional field and defalt value
    # Rating: Optional[int] = None #optional field 

my_posts = [{"title": "post 1", "content": "content of post 1", "id": 1},
            {"title": "post 2", "content": "content of post 2", "id": 2}]

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

@app.post("/post")
def create_post(post: Post):
    print(post)
    print(post.dict()) # converting pydantic model to dictionary
    return {'data': post}

@app.get("/post")
def get_post():
    return {"data": my_posts}

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {'data': post}

def find_post(id):
    for p in my_posts:
        if p["id"]  == id:
            return p

@app.get("/post/{id}")
def get_post(id : int):
# def get_post(id : int, response: Response):
    post = find_post(id)
    if not post:       
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id:{id} was not found"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id:{id} was not found")
    return {"post_detail": post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def updated_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}
