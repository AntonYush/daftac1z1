from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import  Response
from hashlib import sha256
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.sessions = ["admin"]
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
    if request.cookies.get("session_token") not in app.sessions:
        raise HTTPException(status_code=401)
    return {"message": "Welcome there!"}


@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def method_check(request: Request):
    return {"method": request.method}


@app.post("/patient", response_model=PatientPostResp)
def patient_post(request: Request, data: PatientPostRq):
    if request.cookies.get("session_token") not in app.sessions:
        raise HTTPException(status_code=401)
    response = PatientPostResp(id=app.counter, patient=data.dict())
    patients[app.counter] = data.dict()
    app.counter += 1
    return response


@app.get("/patient/{patient_id}")
def patient_get(request: Request, patient_id: int):
    if request.cookies.get("session_token") not in app.sessions:
        raise HTTPException(status_code=401)
    if patient_id in patients.keys():
        return patients[patient_id]
    raise HTTPException(status_code=204)


@app.post("/login")
def login(request: Request):
    response = Response()
    response.status_code = 303
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="session_token", value=request.headers["Authorization"][5:])
    app.sessions.append(request.headers["Authorization"][5:])
    return response


@app.post("/logout")
def logout(request: Request):
    response = Response()
    response.status_code = 303
    response.headers["Location"] = "/"
    app.sessions.pop(app.sessions.index(request.cookies.get("session_token")))
    response.delete_cookie(key="session_token")
    return response
