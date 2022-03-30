#!/bin/sh

isort -q spatiotemporal/ imageannotationsd/
black -q spatiotemporal/ imageannotationsd/
pyflakes spatiotemporal/ imageannotationsd/
mypy --no-color-output --no-error-summary spatiotemporal/ imageannotationsd/
