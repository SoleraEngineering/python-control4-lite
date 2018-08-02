# Control4 API Bindings for Python


## Developers

### Setup

1. Install Python 3 `export PATH=/usr/local/bin:/usr/local/sbin:$PATH; brew install python`
1. Upgrade Pip `pip install --upgrade pip`
1. Install Pipenv `pip install --user pipenv`
1. Install Virtualenv `pip install virtualenv`


### Publish

1. `python setup.py sdist bdist_wheel`
1. `twine upload dist/*`

