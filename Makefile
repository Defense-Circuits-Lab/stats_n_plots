.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

all: dcl_stats_n_plots docs

dcl_stats_n_plots: $(SRC)
	nbdev_build_lib
	touch dcl_stats_n_plots

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	fastrelease_conda_package --upload_user dennis_segebarth
	nbdev_bump_version

conda_release:
	fastrelease_conda_package --upload_user dennis_segebarth

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist