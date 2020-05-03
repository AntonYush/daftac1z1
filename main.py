from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import aiosqlite

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
    response.status_code = 301
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
    raise HTTPException(status_code=204)


@app.post("/login")
def login(request: Request):
    if request.headers.get("Authorization") is None or \
            request.headers.get("Authorization").split()[1] not in app.users.values():
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


class RowFactories(object):
    @staticmethod
    def tracks_get(cursor, x):
        return {"TrackId": int(x[0]),
                "Name": str(x[1]),
                "AlbumId": int(x[2]),
                "MediaTypeId": int(x[3]),
                "GenreId": int(x[4]),
                "Composer": str(x[5]),
                "Milliseconds": int(x[6]),
                "Bytes": int(x[7]),
                "UnitPrice": float(x[8])}

    @staticmethod
    def composers_data_get(cursor, x):
        return str(x[0])


@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect('./dbs/chinook.db')


@app.on_event("shutdown")
async def shutdown():
    await app.db_connection.close()


@app.get("/tracks")
async def tracks_get(page: int = 0, per_page: int = 10):
    app.db_connection.row_factory = RowFactories.tracks_get
    cursor = await app.db_connection.execute(
        f"SELECT * FROM tracks LIMIT {per_page} OFFSET {page*per_page}")
    data = await cursor.fetchall()
    return data


@app.get("/tracks/composers")
async def composers_tracks_get(composer_name: str = None):
    if not composer_name:
        raise HTTPException(status_code=404, detail={"error": "Composer's name needed!"})
    app.db_connection.row_factory = RowFactories.composers_data_get
    cursor = await app.db_connection.execute(
        f"SELECT name FROM tracks WHERE composer = {composer_name} ORDER BY name")
    data = await cursor.fetchall()
    return data
