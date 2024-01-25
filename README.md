# Casting Agency

## Introduction

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.


## Getting Started[Locally]

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies


```bash
pip install -r requirements.txt
```

## Running the server
Check DATABASE_URL in setup.sh is setted correctly
```bash
#!/bin/bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
```

To run the server, execute:
```bash
source setup.sh # set DATABASE_URL as environment variable
export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
flask run
```

## Testing
Check TEST_DATABASE_URL in setup.sh is setted correctly
```bash
#!/bin/bash
export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres_test"
```

To deploy the tests, run

```bash
source setup.sh
dropdb postgres_test
createdb postgres_test
psql postgres_test < postgres_test.psql
python test_app.py
```


### API Reference
#### Base url
`http://127.0.0.1:5000/`

#### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable


#### Endpoints - Actors
`GET '/actors'`
or
`GET '/actors?page=${integer}'`

- Fetches a paginated set of actors, a total number of actors.
- Request Arguments: `page` - integer
- Returns: An object with 5 paginated actors, total actors
- Sample 1: `curl http://127.0.0.1:5000/actors`
- Sample 2: `curl http://127.0.0.1:5000/actors?page=2`

```json
{
  "actors": [
    {
      "age": 59,
      "gender": "Female",
      "id": 9,
      "name": "Sandra Bullock"
    }
  ],
  "success": true,
  "total_actors": 6
}
```


---

`POST '/actors'`

- Sends a post request in order to add a new actor
- Request Body:
```json
{
    "name": "Heres a new actor name string",
    "age": 18,
    "gender": "Heres a new actor gender string"
}
```
- Returns: the information of the created actor
- Sample : `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"Heres a new actor name string", "age": 18, "gender": "Heres a new actor gender string"}'`
```json
{
    "actor": {
    "age": 18,
    "gender": "Heres a new actor gender string",
    "id": 10,
    "name": "Heres a new actor name string"
    },
    "success": true
}
```

---

`PATCH '/actors/${id}'`

- Sends a patch request in order to patch a new actor information using the id of the actors
- Request Arguments: `id` - integer
- Request Body:
```json
{
    "name": "Heres a patched actor name string",
    "age": 18,
    "gender": "Heres a patched actor gender string"
}
```
- Returns: the information of the updated actor
- Sample : `curl http://127.0.0.1:5000/actors/10 -X PATCH -H "Content-Type: application/json" -d '{"name": "Heres a patched actor name string", "age": 18, "gender": "Heres a patched actor gender string"}'`
```json
{
    "actor": {
    "age": 18,
    "gender": "Heres a patched actor gender string",
    "id": 10,
    "name": "Heres a patched actor name string"
    },
    "success": true
}
```
---

`DELETE '/actors/${id}'`

- Deletes a specified actor using the id of the actors
- Request Arguments: `id` - integer
- Returns: Return HTTP status code and id of deleted the actor.
- Sample : `curl -X DELETE http://127.0.0.1:5000/actors/10`
```json
{
    "delete": 10,
    "success": true
}
```
---
#### Endpoints - Movies
`GET '/movies'`
or
`GET '/movies?page=${integer}'`

- Fetches a paginated set of movies, a total number of movies.
- Request Arguments: `page` - integer
- Returns: An object with 5 paginated movies, total movies
- Sample 1: `curl http://127.0.0.1:5000/movies`
- Sample 2: `curl http://127.0.0.1:5000/movies?page=2`

```json
{
  "movies": [
    {
      "id": 6,
      "release_date": "1997-11-01T00:00:00.000Z",
      "title": "Titanic"
    }
  ],
  "success": true,
  "total_movies": 6
}
```


---

`POST '/movies'`

- Sends a post request in order to add a new movie
- Request Body:
```json
{
    "title": "Heres a new movie title string",
    "release_date": "2024-12-25T00:00:00.000Z"
}
```
- Returns: the information of the created actor
- Sample : `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title": "Heres a new movie title string", "release_date": "2024-12-25T00:00:00.000Z"}'`
```json
{
    "movie": {
      "id": 7,
      "release_date": "Heres a new movie release_date string",
      "title": "2024-12-25T00:00:00.000Z"
    }
    "success": true
}
```

---

`PATCH '/movies/${id}'`

- Sends a patch request in order to patch a movie information using the id of the movies
- Request Arguments: `id` - integer
- Request Body:
```json
{
    "title": "Heres a patched movie title string",
    "release_date": "2024-12-26T00:00:00.000Z"
}
```
- Returns: the information of the updated movie
- Sample : `curl http://127.0.0.1:5000/movies/9 -X PATCH -H "Content-Type: application/json" -d '{"title": "Heres a patched movie title string", "release_date": "2024-12-26T00:00:00.000Z"}'`
```json
{
    "movie": {
      "id": 9,
      "release_date": "2024-12-26T00:00:00.000Z",
      "title": "Heres a patched movie title string"
    },
    "success": true
}
```
---

`DELETE '/movies/${id}'`

- Deletes a specified movie using the id of the movies
- Request Arguments: `id` - integer
- Returns: Return HTTP status code and id of deleted the movie.
- Sample : `curl -X DELETE http://127.0.0.1:5000/movies/9`
```json
{
    "delete": 9,
    "success": true
}
```
