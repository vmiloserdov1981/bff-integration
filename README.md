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

Renew snapshots for linux
⚠️THIS STEP MAY DIFFER FOR WINDOWS⚠️
change $PWD to absolute path to work directory

```shell
docker run -v $PWD/tests:/bff-integration/tests -it testrun poetry run pytest --update-snapshots tests/ui
```

Run local UI tests
```shell
docker run -v $PWD/tests:/bff-integration/tests -it testrun poetry run pytest tests/ui
```

Run local API tests
```shell
docker run -v $PWD/tests:/bff-integration/tests -it testrun poetry run pytest tests/api
```

Run local all tests
```shell
docker run -v $PWD/tests:/bff-integration/tests -it testrun poetry run pytest tests
```
## Сравнение скриншотов

Для сравнения скриншотов используется фикстура `assert_snapshot` из плагина `snapshot.py`
Можно было использовать существующий плагин `pytest-playwright-snapshot`
Ссылка на оригинальный плагин: https://github.com/kumaraditya303/pytest-playwright-snapshot

Но существующий плагин не сохраняет изображение с различиями в скриншотах, что кажется важным моментом
Поэтому код перенесён в наш репозиторий и немного изменён.
В случае несовпадения изображений, изображение с различиями сохраняется в папке
`report/snapshots`

### Первичная настройка

Для того чтобы было с чем сравнивать изображения, необходимо инициализировать эталонные изображения,
запустив тесты с параметром `--update-snapshots`
Также этот параметр используется для обновления существующих скриншотов.

### Проверка скриншотов в пайплайне

Поскольку в пайплайне тесты будут запускаться в OS Linux, а плагин для разных ОС сохраняет в разных папках,
для каждого теста, сравнивающего изображения, необходимо инициализировать изображения для `linux`
Это можно сделать следующей командой:
```shell
docker run -v $PWD/tests:/bff-integration/tests -it testrun poetry run pytest --update-snapshots tests/ui
```
При этом изображения для `linux` будут добавлены в локальный репозиторий.
Для OS Windows команда будет отличаться, нужно вместо `$PWD` указать полный путь к рабочей директории,
либо заменить `$PWD` переменной среды в формате Windows, содержащей такой путь.
(Данное предположение ещё не проверялось)

### Примеры

Пример использования сравнения изображений добавлен в тест `tests/ui/login_page/test_login_page_ui.py`
В общем случае использование выглядит как-то так:
```python
assert_snapshot(auth_page.logo_container.screenshot(type='png'), 'login_page_logo.png')
```
