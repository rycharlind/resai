# ResAI

An AI research tool. 

## Py (Backend API)

Python based backend using FastAPI and the core ResAI python modules.

### API

- Terminal: `python src/server.py`
- VS Code: See `launch.json` -> `ResAI Py API`

## Svelte (Frontend App)

A frontend Svelte app for interacting with the Py Backend API.

- Dev: `npm run dev`

# Helper Commands

### Poetry

Helper reference commands for Poetry:

- `poetry env use 3.11.2` - Run this first to make sure you install with the proper Python version in your `.venv`.
- `poetry install` - Install all Python dependencies. 
- `poetry show -l` - Show current deps version along with the latest.
- `poetry add "langchain==0.0.208"` - Update dep to a specific version.
- `poetry config --list` - Show the current poetry config. # ref: https://python-poetry.org/docs/configuration/

## How to create a new Virtual Env (using "supabase" as example name here.):
- `cd virtualenvs` - Navigate to the `virtualenvs` dir local to this project.
- `mkdir supabase` - Create a new directory for the new environment name.
- `virtualenv -p ~/.pyenv/versions/3.11.2/bin/python .venv` - Create a new `virtualenv` from within this dir. 
- `source .venv/bin/activate` - Active the new virtualenv. 
- `poetry init` - Init a new Poetry project. 
- `poetry add <lib>` - Now you can start adding depts with Poetry.  
- `source virtualenvs/supabase/.venv/bin/activate` - You may need to activate the venv from the root of the project in order for VS Code to detect it.


### PyEnv

Helper reference commands for PyEnv:

- `pyenv version` - Check current version.
- `pyenv virtualenv 3.11.2 .venv_2` - create a new virtual env.
- `pyenv install --list | grep " 3\.[11]"` - List all possible Python versions within a family.
- `pyenv install 3.11.2` - Install Python version.
- `ls ~/.pyenv/versions/` or `pyenv versions` - View all installed Python versions.
- `pyenv uninstall 2.7.15` - Uninstall Python versions.
- `pyenv local 3.11.2` - Set the local project Python version.


### Pyenv Refs:
- https://realpython.com/intro-to-pyenv/

