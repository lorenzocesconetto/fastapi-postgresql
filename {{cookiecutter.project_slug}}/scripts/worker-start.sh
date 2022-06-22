#! /usr/bin/env bash
set -eou pipefail

celery --app app.worker worker --loglevel info --queues main-queue --concurrency 1
