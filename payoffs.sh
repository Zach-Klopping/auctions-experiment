#!/bin/bash

export DATABASE_URL=$(heroku config:get DATABASE_URL -a auctions-experiment)
python calculate_payoffs.py
