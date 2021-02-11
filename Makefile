.PHONY: create-env update-env

REPO=$(shell basename $(CURDIR))

create-env: prepare-local
	python3 -m venv .$(REPO);
	. .$(REPO)/bin/activate; \
			pip3 install --upgrade  -r requirements-dev.txt; \
			python setup.py develop;

prepare-local:
	export GOOGLE_APPLICATION_CREDENTIALS=$(base64 /Users/joaoc/gcloud-creds/rj-smtr-credentials.json)

update-env:
	. .$(REPO)/bin/activate; \
	pip3 install --upgrade -r requirements-dev.txt;

attach-kernel:
	python -m ipykernel install --user --name=$(REPO);

release-heroku:
	heroku config:set GOOGLE_APPLICATION_CREDENTIALS=$$(base64 /Users/joaoc/gcloud-creds/rj-smtr-credentials.json)
	git add .
	git commit -m 'release'
	git push heroku main

	
