venv:
	pip install pipx
	pipx ensurepath
	pipx install poetry
	
	poetry init --no-interaction
	poetry add requests
	poetry add python-dotenv
	poetry add splunk-sdk
	poetry shell

splunk_alert:
	python3 Splunk\splunk_alert.py