"""
General API for generating dummy data.
"""
import json
from jsf import JSF
from jsonschema import Draft7Validator
from fastapi import FastAPI, Request, HTTPException
from formatters import JsonFormatter, SQLFormatter
from schema import SCHEMA

app = FastAPI()


@app.post("/seeds")
async def seeds(info: Request):
    """
    Returns a bunch of dummy data based on JSON schema.
    """
    try:
        req_info = json.loads(await info.body())
    except (TypeError, ValueError) as exception:
        raise HTTPException(
            status_code=422, detail="Not a valid JSON") from exception

    validator = Draft7Validator(SCHEMA)
    errors = sorted(validator.iter_errors(req_info), key=str)

    if len(errors) > 0:
        messages = list(map(lambda e: e.json_path + ": " + e.message, errors))
        raise HTTPException(status_code=422, detail={"messages": messages})

    try:
        faker = JSF(req_info["schema"])
    except Exception as exception:
        raise HTTPException(
            status_code=422, detail="Cannot parse schema") from exception

    data = [faker.generate() for _ in range(0, req_info["count"])]

    match req_info["format"]:
        case None | "json":
            formatter = JsonFormatter(req_info["schema"]["title"])

        case "sql":
            formatter = SQLFormatter(req_info["schema"]["title"])

        case _:
            raise HTTPException(status_code=422, detail="Not a valid format")

    return formatter.format(data)
