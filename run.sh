#!/usr/bin/env bash

{ docker-compose up --no-color & sleep 600 && docker-compose rm -f ; } &> logfile.log &
