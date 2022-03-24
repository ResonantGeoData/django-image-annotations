#!/bin/sh

isort -q image_annotations/ imageannotationsd/
black -q image_annotations/ imageannotationsd/
pyflakes image_annotations/ imageannotationsd/
mypy --no-color-output --no-error-summary image_annotations/ imageannotationsd/
