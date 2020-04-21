# scrumsistant
Assistant for Scrum Stuff

## FrontEnd

See the README in the frontend subfolder for setting up the front end but its mostly

[one time] Make sure you have angular CLI installed (https://cli.angular.io/)
    
    npm install -g @angular/cli

[sometimes, including the first time] [in the frontend dir]

    npm ci

Why npm ci?  https://stackoverflow.com/a/53325242

    
[every time], run the front end [in the frontend subdir]
    
    ng serve [--open, will open a tab to the right url for you]
    [itll run for a bit, print out a bunch of shit, eventually you'll get either nice green or red compiler errors]
    
    
    
## BackEnd

[one time, optional] Set up a virtualenv with python3.8 

There's a lot of ways, I use this one (https://virtualenv.pypa.io/en/latest/).  It has a list of wrappers for itself at the bottom, w/e works for you

    [in home dir] virtualenv scrumenv -p python3.8 [assumes python3.8 is installed and on PATH]
    
    source scrumenv/bin/activate [on windows there should be an activate.bat somewhere approximately there that you have to run]
    
    [in backend dir]
    
    pip install -r requirements.txt
    
[every time, in the root dir.  NOTE THIS WILL NOT AUTORELOAD FOR YOU.  IF YOU CHANGE CODE, ctrl+c AND RESTART IT]

    python runserver.py
    [it won't print anything out, its just a run_forever asyncio thing.  Stuff will print out as you navigate around in the app]

## Coding Standards

We are formatting our backend code according to the standards imposed by the fascist maintaining [`black`](https://github.com/psf/black). We are also using the [`isort`](https://github.com/timothycrosley/isort) library. You can easily set up your IDE to auto-run these tools whenever you save, which I suggest (and can help with).

We are also using a cool python library called [`pre-commit`](https://github.com/timothycrosley/isort) that will generate the file `.git/hooks/pre-commit` in your project to automatically do this formatting for you whenever you commit code. Please set this up prior to contributing on the backend by installing `pre-commit` (it's in the `requirements.txt` so should happen when running `pip install -r requirements.txt`) and then running `pre-commit install`, which will actually make the hook file (based on the rules we set up for it in `.pre-commit-config.yaml`). Now, whenever you commit, if your code doesn't adhere to the standards you'll get a scary message like `black..........fail` and then a message that `black` reformatted your code. Don't be too scared, just configure your IDE to auto-run them ahead of time if you don't want to be called a failure every time you make commits.