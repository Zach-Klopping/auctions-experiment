#!/bin/bash

export DATABASE_URL=$(heroku config:get DATABASE_URL -a game-theory-experiment)
python calculate_payoffs.py > payoff_log.txt 2>&1
