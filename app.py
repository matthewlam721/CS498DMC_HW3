import os
from fastapi import FastAPI, Body
from pymongo import MongoClient, WriteConcern, ReadPreference

client = MongoClient(os.environ["MONGO_URI"])
col = client["ev_db"]["vehicles"]
app = FastAPI()


@app.post("/insert-fast", status_code=201)
def insert_fast(doc: dict = Body(...)):
    c = col.with_options(write_concern=WriteConcern(w=1))
    res = c.insert_one(doc)
    return str(res.inserted_id)


@app.post("/insert-safe", status_code=201)
def insert_safe(doc: dict = Body(...)):
    c = col.with_options(write_concern=WriteConcern(w="majority"))
    res = c.insert_one(doc)
    return str(res.inserted_id)


@app.get("/count-tesla-primary")
def count_tesla():
    c = col.with_options(read_preference=ReadPreference.PRIMARY)
    return {"count": c.count_documents({"Make": "TESLA"})}


@app.get("/count-bmw-secondary")
def count_bmw():
    c = col.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    return {"count": c.count_documents({"Make": "BMW"})}