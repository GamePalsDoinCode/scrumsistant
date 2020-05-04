[![Build Status](https://travis-ci.org/GamePalsDoinCode/scrumsistant.svg?branch=master)](https://travis-ci.org/GamePalsDoinCode/scrumsistant)
[![Coverage Status](https://coveralls.io/repos/github/GamePalsDoinCode/scrumsistant/badge.svg?branch=master)](https://coveralls.io/github/GamePalsDoinCode/scrumsistant?branch=master)

# scrumsistant
Assistant for Scrum Stuff

## Frontend

The frontend uses typescript and angular. [See here](#frontend-1) for instructions on how to get started and [here](#frontend-2) for how to run the code after.

## Backend

The backend uses python and redis. [See here](#backend-1) for instructions on how to get started and [here](#backend-2) for how to run the code after.

# Getting Started

## First Time Running Code

### Frontend
* **NPM**
    * Make sure you have node.js and npm [installed](https://www.npmjs.com/get-npm)
* **Angular CLI**
    * Install [angular CLI](https://cli.angular.io) with `npm install -g @angular/cli`
* **Frontend Package Dependencies**
    * Run `npm ci` to install any libraries we need. You will need to do this again whenever new dependencies are added. [Here's why](https://stackoverflow.com/a/53325242) we use this instead of `npm install`.
* **TSLint**
    * Run `npm install tslint typescript -g` to install tslint
### Backend
* **Python Virtual Environment**
    * **Danny:** 
        * [virtualenv](https://virtualenv.pypa.io/en/latest/).  It has a list of wrappers for itself at the bottom, w/e works for you
        * [in home dir] `virtualenv scrumenv -p python3.8` [assumes python3.8 is installed and on PATH]
        * `source scrumenv/bin/activate` [on windows there should be an activate.bat somewhere approximately there that you have to run]
    * **Mike:** 
        * I [configure Pycharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#) to handle this crap for me using `venv`.
* **Backend Python Package Dependencies**
    * After setting up and activating your virtual environment, install all of the python libraries we need using `pip install -r requirements.txt` in the backend dir. You will need to do this again whenever new dependencies are added.
    * We use [pip-tools](https://pypi.org/project/pip-tools/) to freeze our requirements (don't worry, it's included in the requirements). So any time you need to add a new requirement, please add it to the [requirements.in](https://github.com/GamePalsDoinCode/scrumsistant/blob/master/backend/requirements.in) file, then run `pip-compile requirements.in` (or `pip-compile.exe requirements.in` for the Windows heathens) to produce a requirements.txt file with the properly frozen further level requirements.
* **Code Formatting Enforcement**
    * Create a local pre-commit hook by following the [instructions below](#Enforced-formatting-via-pre-commit-hooks).
* **Redis**
    * [Install redis](https://redis.io/topics/quickstart) and, if you're feeling fancy, make it a ["proper service"](https://gist.github.com/hackedunit/a53f0b5376b3772d278078f686b04d38).
        * **Windows note:** I executed the installation commands from the first link in WSL, but now I can only run redis in Ubuntu. This is fine for me but perhaps you would like to find a better solution. Please do! 
    * Start the redis server locally
* **Local Settings**
    * Create a `backend/local_settings.py` file, and populate it like so:
    ```python
    SERVER_NAME = 'me'
    REDIS_URL = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_DB = 0
    FLASK_SECRET_KEY = '' # GENERATE A SECRET KEY
    ```
    * Generate a secret key [like so](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask/34903502#34903502) and then put it in your `local_settings.py` file
* **Make A User**
    * The code requires you have a user before logging in. In the `scripts` directory run `python create_user.py {email} {password}`, which will make a user record in your local redis db.

## Each Time You Run Code

### Backend
* **Redis** (port 6379)
    * Run `redis-cli` to make sure redis is running locally
* **Websocket Server** (port 8000)
    * In root, `python runserver.py`
* **Flask Server** (port 5000)
    * In `backend`, `./run_flask.sh`
### Frontend
* **Angular Server** (port 4200)
    * In `frontend`, `ng serve`

Now you should be able to go to http://localhost:4200/ and login with the [user you created earlier](#make-a-user). 

# Coding Standards

## Formatting

### Frontend
We are using tslint to lint our code. Install it as per the [instructions above](#frontend-1), and then run `tslint --project /path/to/project --config /path/to/project/tslint.json` in the `frontend` directory to run the linter and show you any errors that need to be fixed. If you are using VS Code, consider installing [the extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-tslint-plugin).

### Backend
We are formatting our backend code according to the standards imposed by the fascist maintaining [`black`](https://github.com/psf/black). We are also using the [`isort`](https://github.com/timothycrosley/isort) library. You can easily set up your IDE to auto-run these tools whenever you save, which I suggest (and can help with).

## Enforced formatting via pre-commit hooks
We are also using a cool python library called [`pre-commit`](https://github.com/timothycrosley/isort) that will generate the file `.git/hooks/pre-commit` in your project to automatically do this formatting for you whenever you commit code. 

Please set this up prior to contributing on the backend by installing `pre-commit` (it's in the `requirements.txt` so should happen when running `pip install -r requirements.txt`) and then running `pre-commit install`, which will actually make the hook file (based on the rules we set up for it in `.pre-commit-config.yaml`). 

Now, whenever you commit, if your code doesn't adhere to the standards you'll get a scary message like `black..........fail` and then a message that `black` reformatted your code. Don't be too scared, just configure your IDE to auto-run them ahead of time if you don't want to be called a failure every time you make commits.
