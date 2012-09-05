# Poold.in

This is the primary web app for pooldin. It is currently in early stage
development and should not be placed in a production environment.

All development is assumed to be in on Mac OSX with the following
dependencies:

- [Homebrew][brew]
- [Heroku Toolbelt][toolbelt]
- [Postgresapp][postgresapp] ([docs][postgresapp-docs])
- `[sudo] brew install git node`
- `[sudo] easy_install pip`
- `[sudo] gem install foreman` (See Environment below for details)
- `[sudo] pip install virtualenvwrapper`

You will be working with python virtual environments quite often when
testing different dependencies and working with others. Make sure to configure
and optimize [virtualenv][virtualenv]/[virtualenvwrapper][virtualenvwrapper]
for your workflow.

## Develop

    git clone git@github.com:pooldin/pooldin.git pooldin
    cd pooldin
    mkvirtualenv pooldin
    make init

This installs both production and development dependencies as well as
the database. Check out the `Makefile` to see what was installed and
how the separation between production and development is made.

### Environment

We are currently using Heroku for hosting which means many configuration values
are defined as environment variables. In order to support this
architecture while working locally, they have provided their
[toolbelt][toolbelt].

The heroku gem is useful as is but the [foreman][foreman] gem is out of date.
Specifically, we need the `foreman run` command to support the `--env` flag
so we can specify custom environment files. Currently, this can only be fixed
by installing the foreman gem (which you may have done above):

    [sudo] gem install foreman

We use the `conf` directory to define Procfile and requirements.txt files
for a different environment. The default environment is `dev`. However,
all `make` commands support custom environments via the ENV variable.
For example:

    make ENV=test
    make ENV=test run
    make ENV=test shell

This helps keep environment and Procfile pollution to a minimum as well
as maintains environment state accross different scenarios.

*NOTE:* Due to Heroku constraints, the production Procfile
and requirements.txt are symlinked to their conf/prod counterparts.

Here are the currently required environment variables:

- `POOLDIN_ENV`
- `POOLDIN_DATABASE_URL`
- `POOLDIN_SECRET_KEY`
- `POOLDIN_SESSION_SALT`

### Database

When `make init` is run, it creates the conf/dev/.env environment file.
It assumes that your database uri is:

    postgresql://localhost/pooldin

Make sure to change this uri to your local database uri.

**Commands**

- `make db`
- `make reset`

### Lint

In a perfect world, a release will not go out without a series of
checks. Linting is one of those checks to make sure code is developed in
a consistent mannor.

Until we have the infrastructure in place, we'll have to be good
citizens and check our own belly buttons for lint.

    make lint

### Known Issues

- The `webassets` dependency is on a development version (0.8.dev) to
  make use of correct build and watch functionality.


## Optional Tools

**Python**

- `pip install pyflakes`
- `pip install pep8`

**MacVim**

- `brew install macvim`
- [pathogen][vim-pathogen]
- [nerdtree][vim-nerdtree]
- [syntastic][vim-syntastic]
- [pyflakes-vim][vim-pyflakes]

**Postgres**

- [Induction][postgres-induction]
- [pgAdmin][pgadmin]
- [Navicat][postgres-navicat]


## TODO

**Implement CI**

We need to compile static resources and that is only currently possible
by adding them to git so heroku can pick them up. We need to add a CI
process to correctly deploy and keep build files out of the repo.

For now the resources are being committed to git. This is ugly. We need
to fix this.


[brew]:https://github.com/mxcl/homebrew/wiki/Installation
[pip]:http://www.pip-installer.org/en/latest/index.html
[virtualenv]:http://www.virtualenv.org/en/latest/index.html
[virtualenvwrapper]:http://www.doughellmann.com/projects/virtualenvwrapper/
[foreman]:https://github.com/ddollar/foreman/
[toolbelt]:https://toolbelt.heroku.com/
[postgres-induction]:http://inductionapp.com/
[postgres-navicat]:http://www.navicat.com/en/products/navicat_pgsql/pgsql_overview.html
[postgresapp]:http://postgresapp.com/
[postgresapp-docs]:http://postgresapp.com/documentation
[pgadmin]:http://www.pgadmin.org/
[vim-pathogen]:https://github.com/tpope/vim-pathogen
[vim-pyflakes]:https://github.com/kevinw/pyflakes-vim
[vim-nerdtree]:https://github.com/scrooloose/nerdtree
[vim-syntastic]:https://github.com/scrooloose/syntastic
