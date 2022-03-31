#!/bin/sh
set -ex

service pcscd start

if [[ -n $RUN_WITH_WORKER ]] && $RUN_WITH_WORKER
then
  pipenv run python -m erica.infrastructure.rq.worker&
  exec pipenv run "$@"
else
  exec pipenv run "$@"
fi
