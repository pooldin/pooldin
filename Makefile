# Magical make incantations...
.PHONY := all assets clean css db deps env init js lint npm reset run shell \
		  sql sql-create sql-drop tests

.DEFAULT_GOAL := deps


# Modifiable
ENV=dev
DIR=$(ENV_DIR)
ARGS=$(ENV_ARGS)
PROC=$(ENV_PROC)


# _NOT_ Modifiable
ENV_DIR=.
ENV_CONF=conf/$(ENV)
ENV_ARGS=conf/$(ENV)/.env
ENV_PROC=conf/$(ENV)/Procfile
ENV_REQS=conf/$(ENV)/requirements.txt
ENV_REQS_PROD=conf/prod/requirements.txt

RUN=foreman run -d $(DIR) -e $(ARGS)
START=foreman start -d $(DIR) -e $(ARGS) -f $(PROC)
MANAGE=$(RUN) python manage.py


$(ENV_ARGS):
	@mkdir -p $(@D)
	@touch $@
	@echo 'POOLDIN_ENV=$(ENV)' >> $@
	@echo 'POOLDIN_SESSION_SALT=$(shell python -c "import uuid; print uuid.uuid4().hex")' >> $@
	@echo 'POOLDIN_SECRET_KEY=$(shell python -c "import uuid; print uuid.uuid4().hex")' >> $@
	@echo 'POOLDIN_DATABASE_URL=postgresql://localhost/pooldin' >> $@

$(ENV_REQS):
	@mkdir -p $(@D)
	touch $@

$(ENV_PROC):
	@mkdir -p $(@D)
	@touch $@
	@echo 'web: python manage.py runserver' >> $@

assets:
	@$(MANAGE) assets build --no-cache

clean:
	@find . -name "*.py[co]" -exec rm -rf {} \;
	@$(MANAGE) assets clean

css:
	@$(MANAGE) assets build --no-cache pooldin-css pooldin-css-min

css-debug:
	@$(MANAGE) assets build --no-cache pooldin-css

db:
	@$(MANAGE) createdb || true

deps:
	@$(MAKE) ENV=$(ENV) env

env: $(ENV_ARGS) $(ENV_PROC) $(ENV_REQS)
	@if [ "$(ENV)" == "prod" ]; then \
		pip install -r $(ENV_REQS); \
	else \
		easy_install readline; \
		pip install -r $(ENV_REQS_PROD) -r $(ENV_REQS); \
	fi
	@rm -rf build

init:
	@echo "Setting up npm packages..."
	@$(MAKE) npm 1>/dev/null 2>/dev/null
	@echo "Setting up pip packages..."
	@$(MAKE) ENV=dev env 1>/dev/null
	@$(MAKE) ENV=test env 1>/dev/null
	@$(MAKE) ENV=prod env 1>/dev/null
	@echo "Setting up database..."
	@$(MAKE) db
	@echo "Setting up static resources..."
	@$(MAKE) assets 1>/dev/null 2>/dev/null
	@echo "Done."

js:
	@$(MANAGE) assets build --no-cache pooldin-js pooldin-js-min

js-debug:
	@$(MANAGE) assets build --no-cache pooldin-js

lint:
	@pep8 .
	@echo "Clean as a whistle"

npm:
	@npm install uglify-js less coffee-script

reset:
	@$(MANAGE) resetdb || true

run:
	@$(START)

shell:
	@$(MANAGE) shell

sql:
	@$(MANAGE) printdb

sql-create:
	@$(MANAGE) printcreatedb

sql-drop:
	@$(MANAGE) printdropdb

tests:
	@python test.py
