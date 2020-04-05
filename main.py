from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method")
def get_method():
    return {"method": "GET"}


@app.post("/method")
def post_method():
    return {"method": "POST"}


@app.put("/method")
def put_method():
    return {"method": "PUT"}


@app.delete("/method")
def delete_method():
    return {"method": "DELETE"}
