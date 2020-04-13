# scrumsistant
Assistant for Scrum Stuff

## FrontEnd

See the README in the scrumsistant subfolder for setting up the front end but its mostly

[one time] Make sure you have angular CLI installed (https://cli.angular.io/)
    
    npm install -g @angular/cli
    
[every time], run the front end [in the scrumsistant subdir]
    
    ng serve [--open, will open a tab to the right url for you]
    [itll run for a bit, print out a bunch of shit, eventually you'll get either nice green or red compiler errors]
    
    
    
## BackEnd

[one time, optional] Set up a virtualenv with python3.8 

There's a lot of ways, I use this one (https://virtualenv.pypa.io/en/latest/).  It has a list of wrappers for itself at the bottom, w/e works for you

    [in home dir] virtualenv scrumenv -p python3.8 [assumes python3.8 is installed and on PATH]
    
    source scrumenv/bin/activate [on windows there should be an activate.bat somewhere approximately there that you have to run]
    
    [in backend dir]
    
    pip install -r requirements.txt
    
[every time, in the backend dir.  NOTE THIS WILL NOT AUTORELOAD FOR YOU.  IF YOU CHANGE CODE, ctrl+c AND RESTART IT]

    python main.py
    [it won't print anything out, its just a run_forever asyncio thing.  Stuff will print out as you navigate around in the app]

