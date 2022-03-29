#!/bin/sh
set -ex

service pcscd start

if [ -z "$RUN_ONLY_API" ]; then
  exec pipenv run "$@"
elif [ -z "$RUN_ONLY_WORKER" ]; then
  pipenv run python -m erica.infrastructure.rq.worker&
else
  pipenv run python -m erica.infrastructure.rq.worker&
  exec pipenv run "$@"
fi
