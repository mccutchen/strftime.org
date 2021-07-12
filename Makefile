VENV_PATH      ?= .venv
VENV_DEPS_PATH ?= .venv-deps

build: $(VENV_PATH)
	$(VENV_PATH)/bin/python3 build.py > docs/index.html

update-deps: $(VENV_DEPS_PATH)
	$(VENV_DEPS_PATH)/bin/pip-compile --no-allow-unsafe > requirements.txt

$(VENV_PATH):
	python3 -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/pip install -U pip && $(VENV_PATH)/bin/pip install -r requirements.txt

$(VENV_DEPS_PATH):
	python3 -m venv $(VENV_DEPS_PATH)
	$(VENV_DEPS_PATH)/bin/pip install -U pip && $(VENV_DEPS_PATH)/bin/pip install pip-tools
