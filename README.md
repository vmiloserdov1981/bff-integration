# BFF API and Front E2E Tests

## Install

### Install Pyenv

```shell
brew update
brew install pyenv
brew install pyenv-virtualenv
```

#### Links

* [homebrew](https://brew.sh/)
* [Pyenv](https://github.com/pyenv/pyenv#homebrew-in-macos)

### Install python

##### Show available Python versions
```shell
pyenv install -l
```
##### Install exact version
```shell
pyenv install 3.11.3
```
#### Links
* [pyenv](https://github.com/pyenv/pyenv)

### Create environment

```shell
pyenv virtualenv testenv
```
(creates `testenv` environment)

### Activate environment

```shell
pyenv activate testenv

```

### Install Poetry

In activated environment
```shell
pip install poetry
```

### Install dependencies
```shell
poetry install
```

### Playwright setup
```shell
poetry run playwright install
```

### Pre-commit setup
```shell
pre-commit install
```

## Run tests

### API

```shell
 poetry run pytest tests/api
```

### UI

#### Headless mode (default)
```shell
 poetry run pytest tests/ui
```

#### Headed mode
```shell
 poetry run pytest tests/ui --headed --browser chromium
```
(also supported 'firefox' and 'webkit' options for browser)

## Pre-commit hooks

In order to check code before commit run
```shell
pre-commit
```
