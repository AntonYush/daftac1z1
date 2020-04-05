from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class PatientPostRq(BaseModel):
    name: str
    surename: str


class PatientPostResp(BaseModel):
    id: int
    patient: dict


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


@app.post("/patient", response_model=PatientPostResp)
def patient_post(rq: PatientPostRq):
    app.counter += 1
    print("Before")
    patients[app.counter] = rq.dict()
    print("After")
    return PatientPostResp(id=app.counter, patient=rq.dict())


@app.get("/patient/{patient_id}")
def patient_get(patient_id):
    patient_id = int(patient_id)
    return {"id": patient_id, "all_ids": str(patients.keys())}
