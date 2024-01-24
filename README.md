


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
echo "setup.sh script executed successfully!"
```

To run the server, execute:
```bash
source setup.sh # set DATABASE_URL as environment variable
export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
flask run
```