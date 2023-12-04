# Lesson2

### Requirements
- Python version >= 3.11 required
- Presence of a virtual environment
- Ubuntu 22.04

### File descriptions

* `app` - the main directory for working with the app
* * `app/api/` - directory with files from API
* * `app/utils/` - directory with help work logic and validation
* * `app/app.py` - main application settings file
* `conf` - directory with configuration files
* `tests` - directory with pytest
* `.gitignore` - file with settings for GIT
* `config.py` - configuration setup file
* `manage.py` - file for launching the application and auxiliary services
* `README.md` - project description file
* `requirements.txt` - libraries to install
* `run.sh` - file for convenient launching of auxiliary services and test environment

### Functionality Description

* The main task of the service is to save raw data and convert to avro format

### Installation

#### Project
* Install git and get project

``` shell
git clone -b lesson2 git@github.com:t4kq1995/data-engineering.git
```

* Installation of virtual environment

``` shell
apt install virtualenv
virtualenv -p python3 venv
. venv/bin/activate
```

* Installation of dependencies

``` shell
pip install -r requirements.txt
```

### Project entry points
* `./run.sh first_app` -- to run API server for save raw data
* `./run.sh second_app` -- to run API server for convert raw data to Avro
* `./run.sh freeze` -- to save requirements
* `./run.sh pylint` -- to start pylint validator
* `./run.sh tests` -- to start pytest


