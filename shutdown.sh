#!/bin/bash

heroku ps:scale web=0 worker=0
heroku addons:destroy heroku-postgresql --confirm game-theory-experiment
