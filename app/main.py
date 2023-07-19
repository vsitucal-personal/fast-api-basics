import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from typing import Union
from fastapi import FastAPI, Header, Query, Request, HTTPException
from models.models import LoginCreds, PersonModelWithFields, NestedPersonWithCreds, MultiParam

spark = SparkSession \
            .builder \
            .appName("SampleTxnRepo") \
            .getOrCreate()
app = FastAPI()


@app.get(path="/", status_code=201)
async def read_root():
    return {"message": "Hi from root"}


@app.get(path="/path_params/{path_param_name}")
async def path_params(path_param_name: int):
    return {"path_param_name": path_param_name}


@app.get(path="/query_params")
async def query_params(
    needy: str,
    bbn: Union[str, None] = None,
    actual_date: Union[str, None] = Query(default=None),
):
    return {
        "bbn": bbn,
        "actual_date": actual_date,
        "needy": needy,
    }


@app.post(path="/headers")
async def headers(
    sample_header1: Union[str, None] = Header(default=None),
    sample_header2: Union[str, None] = Header(default=None, convert_underscores=False)
):
    return {
        "sample_header1": sample_header1,
        "sample_header2": sample_header2
    }


@app.post(path="/request_body", response_model=LoginCreds)
async def request_body(creds: LoginCreds):
    return creds


@app.post(path="/request_body/fields", response_model=PersonModelWithFields)
async def request_body_fields(person: PersonModelWithFields):
    return person


@app.post(path="/request_body/multi_params", response_model=MultiParam)
async def request_body_multi_params(
    person: PersonModelWithFields,
    creds: LoginCreds
):
    return {
        "person": person,
        "creds": creds
    }


@app.post(path="/request_body/nested")
async def request_body_nested(
    person_with_creds: NestedPersonWithCreds
):
    return person_with_creds


@app.post(path="/handling_errors")
async def handling_errors(
    error: bool
):
    if error:
        raise HTTPException(status_code=400, detail="I raised an error")
    return {
        "detail": "no errors"
    }


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get(path="/table_contents")
async def get_table_contents(
    query_date: Union[str, None] = None,
    bbn: Union[str, None] = None,
):
    df = spark.read.format("csv").option("header", "true").load("/code/fast-api-basics/app/file.csv")
    if query_date is not None:
        df = df.filter(f.col("business_date") == query_date)
    if bbn is not None:
        df = df.filter(f.col("bbn") == bbn)

    result_list = df.rdd.map(lambda row: row.asDict()).collect()

    if not result_list:
        return HTTPException(status_code=404, detail="record not found!", headers=None)
    else:
        return result_list
