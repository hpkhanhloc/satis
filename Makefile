.PHONY: install-requirements
install-requirements:
	pip install -r requirements.txt

.PHONY: run-api-locally
run-api-locally: install-requirements
	uvicorn main:app --reload