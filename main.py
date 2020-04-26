from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.users = {"trudnY": "dHJ1ZG5ZOlBhQzEzTnQ="}
app.patients = dict()
templates = Jinja2Templates(directory="templates")


class PatientPostRq(BaseModel):
    name: str
    surname: str


@app.get("/")
def main_page():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome_page(request: Request):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users.values():
        raise HTTPException(status_code=401)
    username = "there"
    for key in app.users.keys():
        if app.users[key] == request.cookies.get("session_token"):
            username = key
            break
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})


@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def method_check(request: Request):
    return {"method": request.method}


@app.post("/patient")
def patient_post(request: Request, data: PatientPostRq):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users.values():
        raise HTTPException(status_code=401)
    response = Response()
    response.status_code = 303
    response.headers["Location"] = f"/patient/{app.counter}"
    app.patients[app.counter] = data.dict()
    app.counter += 1
    return response


@app.get("/patient")
def patient_get(request: Request):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users.values():
        raise HTTPException(status_code=401)
    result = dict()
    for patient_id in app.patients.keys():
        result[f"id_{patient_id}"] = app.patients[patient_id]
    return result


@app.get("/patient/{patient_id}")
def patient_get_id(request: Request, patient_id: int):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users.values():
        raise HTTPException(status_code=401)
    if patient_id in app.patients.keys():
        return app.patients[patient_id]
    raise HTTPException(status_code=204)


@app.delete("/patient/{patient_id}")
def patient_delete_id(request: Request, patient_id: int):
    if request.cookies.get("session_token") is None or \
            request.cookies.get("session_token") not in app.users.values():
        raise HTTPException(status_code=401)
    if patient_id in app.patients.keys():
        del app.patients[patient_id]
    return Response()


@app.post("/login")
def login(request: Request):
    if request.headers.get("Authorization").split()[1] not in app.users.values():
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
