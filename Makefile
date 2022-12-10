
include .env

.PHONY: up

run-local:
	pipenv run uvicorn src.main:app --reload


# mock:


