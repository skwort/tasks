# TASKS
TASKS is a simple web-based task management application that allows users to
create, update, delete, and organise tasks across multiple categories.

![Demo of application](assets/demo.png)

TASKS uses Flask for the REST API and backend, and VanillaJS with SortableJS
for the front-end. State is stored in a SQLite database.

## Installation
First make a virtual environment and install the dependencies.
```
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

If you're working on development locally, you can run the debug server with:
```
flask -A tasks run --debug
```

If you plan on serving this non-locally I'd suggest using a WSGI. I'm currently
using Gunicorn, which is included in the `requirements.txt`. You can run it
using:
```
gunicorn -w 2 -b 0.0.0.0:8000 "tasks:create_app()"
```

I'm using [Caddy][1] as reverse-proxy to expose the service on my homelab.

## Testing
Tests for the REST API are implemented using `pytest`. Use the following command
to run the tests and generate a coverage report:
```
pytest -v --cov=app --cov-report=html
```

## Nix
A nix flake is included in this repo. The dev shell can be run using:
```sh
nix develop
```

The application itself, i.e. flask application, can be served using
```sh
nix run
```
which will use `gunicorn` to serve the application on localhost. Arguments
for `gunicorn` can be passed in via the command line:
```sh
nix run . -- -w 2 -b 0.0.0.0:8000
```

An options module is also available. Refer to `module.nix` for the available
options. Here is how I use it in my config:
```nix
# tasks.nix
{inputs, pkgs, ...}:
{
  imports = [ inputs.tasks.nixosModules.tasks ];
  services.tasks.enable = true;
  services.tasks.user = "sam";
  services.tasks.group = "users";
  services.tasks.dbPath = /data/config/tasks;
  services.tasks.bindIp = "0.0.0.0";
  services.tasks.bindPort = 8000;
  services.tasks.workers = 2;
  services.tasks.package = inputs.tasks.packages.${pkgs.system}.tasks;
}
```

I import this into my main `configuration.nix`. You may need to setup the dbPath
folder.

[1]:https://caddyserver.com/

