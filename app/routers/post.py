from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",   # + id = /posts/{id}
    tags=['Posts']
)

'''
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() # posts = db.query(models.Post) ; print(posts) gives SQL Query ex: select * from posts
    return {"data": posts}
'''

'''
@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}
'''

#@router.get("/") 
@router.get("/", response_model=List[schemas.PostOut]) # and return posts in example.txt 2, without response_model and return results in example.txt 1
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # limit this post to print, skip for to skip starting post
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(posts)
    #posts = db.query(models.Post).all() # for all user post
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # Query parameters in url : {{URL}}posts?limit=3 means telling to get 3 posts only
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #select posts.*, COUNT(votes.post_id) as likes from posts left join votes on posts.id = votes.post_id where group by posts.id;
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # join default is left inner join
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # join default is left inner join
    return posts
    #return {"data": my_post}

'''
@app.post("/createposts")
def createposts(payLoad: dict = Body(...)):
    print(payLoad)       
    return {"new_post": f"title:- {payLoad['title']}, content:- {payLoad['content']}"}
'''
'''
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createposts(post: Post):         #(payLoad: dict = Body(...))
    #print(post)                      # new_post.title for particular data
    #print(post.dict())               #convert to dict
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_post.append(post_dict)
    #return {"data": post}
    return {"data": post_dict}
'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createposts(post: schemas.PostCreate, db: Session = Depends(get_db) ,current_user: int = Depends(oauth2.get_current_user)):  # Provide access token and user supposed to login to create a post: get_current_user: int = Depends(oauth2.get_current_user)
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    
    #new_posts = models.Post(title=post.title, content=post.content, published=post.published) #instead for like this use below
    new_posts = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@router.get("/latest")
def get_latest_post():
    post = my_post[len(my_post) - 1]
    return {"details" : post}

'''
@app.get("/posts/{id}")
def get_post(id: int): #, response: Response): #for without HTTPException
    post = find_post(id)
    if not post:
        #response.status_code = 404           # if {id} is unknow value 

        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id: {id} was not found"}  #2 line equal to below 1 line
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return {"post_details" : post}
'''
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #, response: Response): #for without HTTPException
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return post

'''
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int): 
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist") 
    my_post.pop(index)
    #return {"message" : "Post was succesfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) #if we don't want send any data back
'''

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False) 
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #if we don't want send any data back

'''
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist") 
    post_dict=post.dict()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data" : post_dict}
'''

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s,published = %s WHERE id = %s  RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist") 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()