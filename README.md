# BFF API and Front E2E Tests

## Install

### Install Pyenv

#### MacOS
```shell
brew update
brew install pyenv
brew install pyenv-virtualenv
```
#### Windows
```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
#### Linux
```shell
curl https://pyenv.run | bash
```
#### Links
* [homebrew](https://brew.sh/)
* [pyenv](https://github.com/pyenv/pyenv)
* [pyenv in MacOS](https://github.com/pyenv/pyenv#homebrew-in-macos)
* [pyenv-win](https://github.com/pyenv-win/pyenv-win#quick-start)

### Install python

##### Show available Python versions
```shell
pyenv install -l
```
##### Install exact version
```shell
pyenv install 3.11.3
```

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
poetry run pre-commit install
```

## Run tests

Copy env.example to .env
```shell
cp env.example .env
```

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
poetry run pre-commit
```

## Run tests in Docker

#### It's necessary to have GitLab access token with Docker container registry permissions to run tests from prepared container
[Get token instruction](https://gitlab.c2g.pw/help/user/profile/personal_access_tokens)

### Login GitLab Docker registry

```bash
docker login registry.c2g.pw -u <username> -p <access token>
```

### Renew framework container in Docker registry
⚠️ATTENTION! LONG PROCEDURE! PERFORM ONLY IN CASE OF BIG CHANGES IN FRAMEWORK! ⚠️

Build image
```shell
docker build -t registry.c2g.pw/qa/bff-integration -f Dockerfile.main .
```

Push image
```shell
docker push registry.c2g.pw/qa/bff-integration
```
### Run tests locally

Build for tests
```shell
docker build . -f Dockerfile.tests -t testrun
```

Run UI tests
```shell
docker run -it testrun poetry run pytest tests/ui
```

Run API tests
```shell
docker run -it testrun poetry run pytest tests/api
```
