#!/bin/bash
set -ex

# Set environment variables for cron job (loaded automatically by python-dotenv)
rm -f /app/.env
touch /app/.env
set +x  # Turn off command logging to avoid leaking secrets
echo "PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE" >> /app/.env
echo "PYTHONUNBUFFERED=$PYTHONUNBUFFERED" >> /app/.env
echo "ERICA_ENV=$ERICA_ENV" >> /app/.env
echo "ERICA_DATABASE_URL=$ERICA_DATABASE_URL" >> /app/.env
set -x  # Turn command logging back on

service pcscd start

if [[ $RUN_WITH_WORKER == "True" ]]
then
  pipenv run python -m erica.infrastructure.rq.worker&
  exec pipenv run "$@"
else
  exec pipenv run "$@"
fi
