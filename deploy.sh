#!/bin/bash

git checkout main
git pull


heroku login
heroku git:remote -a game-theory-experiment
git push -f heroku main


heroku addons:create heroku-postgresql:standard-0
heroku ps:scale web=1:standard-1x

