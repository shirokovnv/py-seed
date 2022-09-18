# py-seed

![ci.yml][link-ci]

Minimalistic data seeder, written in python.

The service generates a list of dummy data from [JSON schema](https://json-schema.org/) provided in single API method.

Python version: `3.10`

## Dependencies

- [Docker][link-docker]
- [Make][link-make]
- [FastAPI][link-fastapi]
- [JSON Schema Faker][link-faker]

## Project setup

**From the project root, inside shell, run:**

- `make pull` to pull latest images
- `make install` to install fresh dependencies
- `make up` to run app containers

Now you can visit [`localhost:8000`](http://localhost:8000) from your browser.

- `make down` - to extinguish running containers
- `make help` - for additional commands

## Usage

**Make a post request to `http://localhost:8000/seeds`**

_Options_:

- `format`: Wether response data returned in `json` or `sql` (defaults to `json`)
- `count`: The number of seeds (min: 1, max: 100)
- `schema`: your JSON schema

### Request

```bash
curl --location --request POST 'http://localhost:8000/seeds' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "count": 1,
    "format": "json",
    "schema": {
    "title": "products",
    "type": "object",
    "properties": {
        "productId": {
            "type": "integer"
        },
        "title": {
            "type": "string"
        }
    },
    "required": [ "productId", "title" ]
}}'
```

### Response

```json
{
    "products": [
        {
            "productId": 9963,
            "title": "molestias, Hic"
        }
    ]
}
```

## License

MIT. Please see the [license file](LICENSE.md) for more information.

[link-ci]: https://github.com/shirokovnv/py-seed/actions/workflows/ci.yml/badge.svg
[link-docker]: https://www.docker.com/
[link-make]: https://www.gnu.org/software/make/manual/make.html
[link-faker]: https://github.com/json-schema-faker/json-schema-faker
[link-fastapi]: https://fastapi.tiangolo.com/
