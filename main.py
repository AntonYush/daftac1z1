from fastapi import FastAPI, HTTPException, Request, Cookie
from fastapi.responses import RedirectResponse, JSONResponse
from hashlib import sha256
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
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
def welcome_page():
    return {"message": "Welcome there!"}


@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def method_check(request: Request):
    return {"method": request.method}


@app.post("/patient", response_model=PatientPostResp)
def patient_post(rq: PatientPostRq):
    response = PatientPostResp(id=app.counter, patient=rq.dict())
    patients[app.counter] = rq.dict()
    app.counter += 1
    return response


@app.get("/patient/{patient_id}")
def patient_get(patient_id):
    patient_id = int(patient_id)
    if patient_id in patients.keys():
        return patients[patient_id]
    raise HTTPException(status_code=204)


class LoginRq(BaseModel):
    login: str
    password: str


@app.post("/login")
def login(request: LoginRq):
    response = RedirectResponse("/welcome", status_code=200)
    cookie_v = sha256(bytes("{}:{}".format(request.dict()["login"], request.dict()["password"]), "utf-8")).hexdigest()
    response.set_cookie(key="session_token", value=cookie_v)
    return response
@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def method_check(request: Request):
    return {"method": request.method}


@app.post("/patient", response_model=PatientPostResp)
def patient_post(rq: PatientPostRq):
    response = PatientPostResp(id=app.counter, patient=rq.dict())
    patients[app.counter] = rq.dict()
    app.counter += 1
    return response


@app.get("/patient/{patient_id}")
def patient_get(patient_id):
    patient_id = int(patient_id)
    if patient_id in patients.keys():
        return patients[patient_id]
    raise HTTPException(status_code=204)


@app.post("/login")
def login(request: Request):
    response = RedirectResponse("/welcome")
    response.set_cookie(key="session_token", value=request.headers["Authorization"][5:])
    return response

