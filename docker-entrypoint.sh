#!/bin/bash

flask db upgrade

gnunicorn --bind 0.0.0.0:80 "app:create_app()"