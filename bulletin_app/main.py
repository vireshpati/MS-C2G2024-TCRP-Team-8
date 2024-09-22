from fastapi import Depends, FastAPI, HTTPException
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/bulletin/create/", response_model=schemas.Request)
def create_request(
    request: schemas.RequestCreate,
    uid: str        # fix this
):
    return crud.create_request(request=request, uid=uid)

@app.get("/bulletin/", response_model=list[schemas.Request])
def get_request_list(
    sort_field: str,
    asc: bool,
    filter_tag: str,
    page: int = 1, 
    limit: int = 20,
    resolved_requests: bool
):
    return crud.get_request_list(
        sort_field=sort_field, 
        asc=asc, 
        filter_tag=filter_tag, 
        page=page, 
        limit=limit, 
        resolved_requests=resolve_requests
    )


@app.get("/bulletin/{post_uid}/", response_model=schemas.Request)
def get_request_comments(post_uid: int):
    request = crud.get_request(post_uid)
    return request

@app.post("/request/comments", response_model=schemas.Comment)
def create_comment(
    request: schemas.CommentCreate,
    uid: str        # fix this, put user's
):
    return crud.create_request(request=request, uid=uid)

def edit_request():
    pass

def resolve_request():
    pass

def delete_request():
    pass