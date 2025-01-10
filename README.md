# README
## setup
* clone the repo
* create a virtualenv using `python -m venv [VENV]`
* activate venv using `source [VENV]/bin/activate`
* install packages using `python -m pip install -r requirements.txt `
* run using `DB_USERNAME=[DB_USERNAME] DB_PASSWORD=[DB_PASSWORD] python -m flask --app main run`

## running in production
* run using `DB_USERNAME=[DB_USERNAME] DB_PASSWORD=[DB_PASSWORD] waitress-serve --host 0.0.0.0 main:app`
