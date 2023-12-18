#!/bin/bash
cd ..
if [[ "${1}" == "celery" ]]; then
  celery --app=app.scripts.mail:celery_worker worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=app.scripts.mail:celery_worker flower
  fi