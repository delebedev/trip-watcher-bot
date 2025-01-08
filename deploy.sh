#!/usr/bin/env bash

rm trip-watcher-bot-lambda.zip

VENV_PATH=$(pipenv --venv)
cd "$VENV_PATH/lib/python3.13/site-packages"
zip -r ${OLDPWD}/trip-watcher-bot-lambda.zip .
cd ${OLDPWD}

zip trip-watcher-bot-lambda.zip trip_watcher_bot.py

aws lambda update-function-code --function-name arn:aws:lambda:eu-central-1:836908867991:function:TripWatcherBot --zip-file fileb://trip-watcher-bot-lambda.zip --no-cli-pager