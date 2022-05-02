#!/bin/sh

isort -q spatiotemporal/ pannotationsd/
black -q spatiotemporal/ pannotationsd/
pyflakes spatiotemporal/ pannotationsd/
mypy --no-color-output --no-error-summary spatiotemporal/ pannotationsd/
