from fastapi import FastAPI, HTTPException
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
    patients[app.counter] = rq.dict()
    return PatientPostResp(id=app.counter, patient=rq.dict())


@app.get("/patient/{patient_id}")
def patient_get(patient_id):
    patient_id = int(patient_id)
    if patient_id in patients.keys():
        return {"name": patients[patient_id]["name"],
                "surename": patients[patient_id]["surename"]}
    raise HTTPException(status_code=404, detail="Not found")
