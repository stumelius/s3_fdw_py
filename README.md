# s3_fdw_py

This project implements a PostgreSQL 11.1+ [foreign data wrapper (fdw)](https://wiki.postgresql.org/wiki/Foreign_data_wrappers) for columnar data files stored on [Amazon S3](https://aws.amazon.com/s3/) using Python 3 and [multicorn](https://github.com/Kozea/Multicorn).

## Getting started

### Prerequisites

* PostgreSQL 11.1+
* Python 3.6
* Multicorn
* Docker for end-to-end testing

### Installing

Install dependencies:

```bash
apt-get install postgresql-server-dev-11
```

Install the Python package in a virtual environment:

```bash
git clone https://...
cd s3_fdw_py
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Running the tests

Build and start a `postgresql-multicorn` Docker container for end-to-end testing:

```bash
docker build -t postgresql-multicorn .
docker run -e POSTGRES_USER=pytest -e POSTGRES_PASSWORD=pytest -e POSTGRES_DB=pytest -p 5432:5432 --rm -d postgresql-multicorn
```

Run the test suite:
```bash
pytest
```
