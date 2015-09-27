#!/bin/bash
cd "$RINGO_PROJECT_PATH" || exit
source env/bin/activate
cd Ringo/ || exit
python manage.py ejabberd_auth "$@"
