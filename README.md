# Spice Life Backend Service

## SL CMS

SL CMS is an application that manages SL content.

## Launching the development environment

### Clone and install dependencies

```bash
$ clone the project
$ cd sl-backend
$ python -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Setup a local database

SQLite is currently used as a database, so no action is needed to setup a new one.

### Run the service after activating the virtualenv

```bash
$ python manage.py runserver
```

## Run tests

Install test dependencies

```bash
$ pip install -r test_requirements.txt
```

Make sure your .env file is set to use the `root` database user to run tests

```bash
$ python manage.py test
```

## Run pylint and code formatter

Install test dependencies

```bash
$ pip install -r test_requirements.txt
```

To run pylint execute

```bash
$ PYTHONPATH=$(pwd):$PYTHONPATH DJANGO_SETTINGS_MODULE=sl_backend.settings pylint sl_backend inventory user_management
```

For blue in check mode

```bash
$ blue --check --diff  sl_backend inventory user_management
```

If you want blue to auto-format your code use

```bash
$ blue sl_backend inventory user_management
````
