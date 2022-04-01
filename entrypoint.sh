#!/bin/bash
set -ex

service pcscd start

if [[ $RUN_WITH_WORKER == "True" ]]
then
  pipenv run python -m erica.infrastructure.rq.worker&
  exec pipenv run "$@"
else
  exec pipenv run "$@"
fi
