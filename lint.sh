#!/bin/sh

isort -q spatiotemporal/ pannotations/ pannotationsd/
black -q spatiotemporal/ pannotations/ pannotationsd/
pyflakes spatiotemporal/ pannotations/ pannotationsd/
mypy --no-color-output --no-error-summary spatiotemporal/ pannotations/ pannotationsd/
