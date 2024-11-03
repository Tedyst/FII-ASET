#!/bin/sh

exec celery -A backend worker -l info --max-tasks-per-child=1000
