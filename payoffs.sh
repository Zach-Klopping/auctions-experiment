export DATABASE_URL=$(heroku config:get DATABASE_URL -a auctions-experiment)
python payoffs.py
