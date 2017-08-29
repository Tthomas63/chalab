Chalab
======

Requires:
- docker

For development (running the tests):

- `python3.5`
- an env with the content of the `requirements.txt` (`pip install -r requirements.txt`).
- `phantomjs` for browser testing. Other drivers (Firefox, Chrome, etc) can be used too.


Structure
---------

- `chalab`: core of the project,
- `landing`: the home page app,
- `wizard`: the wizard app,
- `user`: user profile app,
- `bundler`: the challenge -> bundles (zipfiles) app,
- `instances`: the module containing the settings per environment:
    - `local`: the settings to run django on your local machine,
    - `local_docker`: the settings to run django in docker on your local machine (preferred way),
    - `production.py`: settings in production.
- `templates`: global templates,
- `datasets`: default datasets from [automl](http://automl.chalearn.org/data).


We use Celery + RabbitMQ to schedule long running tasks like creating the bundles.
    

Local Dev
---------

The most straightforward way to run chalab is to use docker and docker-compose. It will
start the system (database, server, etc) automatically.

Then you can run the tests on your local machine (non-dockerized) to get assistance from your IDE.
As of now it's not possible to run the tests inside Docker (Pull-Requests are welcome!).


### Start the server:

In the chalab folder,

`make dev` 

It downloads all the containers & dependencies then start the containers.
Access the app at [http://localhost:8000/](http://localhost:8000/).
Kill it (ctrl-c) then re-run `make dev` to rebuild the container and apply db migrations.

### Management

- `make superuser`: when you started the database (`make dev` does it for you)
- `make static`: to re-generate the static resources
- `make migrations`: to generate the django migrations


### Datasets

Chalab comes with a few datasets by defaults, we don't store them in the git repository.

- `make predload_db`: setup the database with datasets and metrics:
    - `make dataset`: download the default datasets locally and add them to the database,
    - `make metrics`: generate the default metrics options and add them to the database.
    
Note that you should these commands only once or you'll have duplicates.

### Testing: setup

Install django, selenium & other dependencies locally.

```
# in your venv:
pip install -r requirements.txt
```


### Run the tests

```
# while the server is running using `make dev':
make test

# clean the data produced by tests
make clean
```

- You can override the selenium ENVs used by `tests/selen.py` to use different drivers,
  by default, you need `phantomjs` installed.
- `chrome` requires the [`chromedriver`](https://sites.google.com/a/chromium.org/chromedriver/)
  to be accessible from your `PATH`.
- `firefox` tends to break if you use the last version.
- `phantomjs` (default) is a safe choice but you won't see the interactions live.


Deployment
----------

Pull the repo, copy the `example.env` to `.env`, then adapt it to your system.
Then run `make prod`

- The production app server will be available at `127.0.0.1:8742`
- The production static server will be available at `127.0.0.1:8842`

Both will be ready to be accessed behind a reverse proxy such as nginx (standard gunicorn setup).
