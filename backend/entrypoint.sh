#!/bin/sh

echo "Waiting for Flask..."

gunicorn -b 0.0.0.0:5000 app:app
