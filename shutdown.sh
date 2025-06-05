#!/bin/bash

heroku ps:scale web=0 worker=0 -a game-theory-experiment
heroku addons:destroy heroku-postgresql --confirm game-theory-experiment
heroku addons:destroy heroku-redis --confirm game-theory-experiment

