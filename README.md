SCANNER BACKEND
============

## Requirements

* Python 3.6
* Virtualenv (created and activated)


## Setup

```
git clone git@github.com:politicalwatch/scanner-backend.git
cd scanner-backend
pip install -r requirements_dev.txt
set -a
source .env
python setup.py develop
```

Finally, edit *scanner_backend/settings.py* file with your specific values.


## Load data

*Pending*


## Run

```
python scanner_backend/app.py
```


## Load testing

For exec load testing is necessary install locust. You can initialize the tool:

```
$ locust Labeling
```

This start local server in port 8089.


## Run tests from docker

With docker-compose executing, you should exec the next command:

```
docker exec -ti scanner-backend sh runtests.sh
```

If you only want to execute one test, you can restrict pytest with -k option:

```
docker exec -ti scanner-backend pytest -v -s --cov-report html --cov=scanner_backend tests -k TestLimit
```
