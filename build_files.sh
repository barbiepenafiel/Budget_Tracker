#!/bin/bashecho "Build script started..."# Install dependenciespip install -r requirements.txt# Collect static filespython manage.py collectstatic --noinput# Run migrationspython manage.py migrate
echo "Build script completed!"
