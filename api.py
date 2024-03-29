"""
General API for generating dummy data.
"""
import json

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from jsf import JSF
from jsonschema import Draft7Validator

from formatters import JsonFormatter, XMLFormatter
from schema import req_schema

app = FastAPI()


@app.post('/seeds')
async def seeds(request: Request) -> Response:
    """
    Seed API endpoint.

    Args:
        request: A JSON request

            _Options:_

            - `format`: **xml** or **json** (default)

            - `count`: number in range(1..100)

            - `schema`: JSON schema

    Returns:
        A list of dummy data based on JSON schema.

    Raises:
        HTTPException: Mostly with status=422.
    """
    try:
        req_info = json.loads(await request.body())
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Not a valid JSON') from exc

    validator = Draft7Validator(req_schema)
    errors = sorted(validator.iter_errors(req_info), key=str)

    if errors:
        messages = ['{0}:{1}'.format(error.json_path, error.message) for error in errors]
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'messages': messages})

    try:
        faker = JSF(req_info['schema'])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Cannot parse schema') from exc

    json_data = [faker.generate() for _ in range(0, req_info['count'])]

    formatter = _choose_formatter(req_info.get('format'), req_info['schema']['title'])

    if isinstance(formatter, XMLFormatter):
        return Response(formatter.format(json_data), media_type='application/xml')

    return JSONResponse(formatter.format(json_data))


def _choose_formatter(input_format: str, schema_title: str) -> JsonFormatter | XMLFormatter:
    """
    Choose formatter by user input format and schema title.

    Args:
        input_format: The format of data output
        schema_title: The name of the schema

    Returns:
        Json or XML formatter.
    """
    match input_format:
        case 'xml':
            return XMLFormatter(schema_title)

        case _:
            return JsonFormatter(schema_title)
