
deps-install:
	@py -m pip install -r requirements.txt

run: deps-install
	@py run.py

test:
	@py -m unittest discover -s tests