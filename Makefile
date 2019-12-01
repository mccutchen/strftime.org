.PHONY: build

build: .venv
	.venv/bin/python3 build.py > docs/index.html

.venv:
	python3 -m venv .venv
	.venv/bin/pip3 install -r requirements.txt
