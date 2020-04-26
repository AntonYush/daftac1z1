from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from hashlib import sha256
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.users = ["dHJ1ZG5ZOlBhQzEzTnQ="]
patients = dict()


class PatientPostRq(BaseModel):
    name: str
    surename: str


class PatientPostResp(BaseModel):
    id: int
    patient: dict


@app.get("/")
def main_page():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome_page(request: Request):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users:
        raise HTTPException(status_code=401)
    print(request.cookies)
    print(request.cookies.get("session_token"))
    print(app.users[0])
    return {"message": "Welcome there!"}


@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def method_check(request: Request):
    return {"method": request.method}


@app.post("/patient", response_model=PatientPostResp)
def patient_post(request: Request, data: PatientPostRq):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users:
        raise HTTPException(status_code=401)
    response = PatientPostResp(id=app.counter, patient=data.dict())
    patients[app.counter] = data.dict()
    app.counter += 1
    return response


@app.get("/patient/{patient_id}")
def patient_get(request: Request, patient_id: int):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users:
        raise HTTPException(status_code=401)
    if patient_id in patients.keys():
        return patients[patient_id]
    raise HTTPException(status_code=204)


class LoginRq(BaseModel):
    login: str
    password: str


@app.post("/login")
def login(request: Request):
    if request.headers.get("Authorization").split()[1] not in app.users:
        raise HTTPException(status_code=401)
    response = Response()
    response.status_code = 303
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="session_token", value=request.headers.get("Authorization").split()[1])
    return response


@app.post("/logout")
def logout():
    response = Response()
    response.status_code = 303
    response.headers["Location"] = "/"
    response.delete_cookie(key="session_token")
    return response
