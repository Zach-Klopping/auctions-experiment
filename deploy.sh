#!/bin/bash

git checkout main
git pull


heroku login
heroku git:remote -a game-theory-experiment
git push -f heroku main


heroku addons:create heroku-postgresql:standard-0
heroku ps:scale web=1:standard-1x
APP_NAME="game-theory-experiment"
ADDON_NAME="heroku-postgresql"

echo "Waiting for $ADDON_NAME addon to finish provisioning..."

while true; do
  STATUS=$(heroku addons -a $APP_NAME | grep $ADDON_NAME | awk '{print $NF}')
  if [[ "$STATUS" == "created" || "$STATUS" == "attached" ]]; then
    echo "$ADDON_NAME is ready."
    break
  else
    echo "Current status: $STATUS. Waiting 10 seconds..."
    sleep 10
  fi
done

echo "You can now run your database commands."
