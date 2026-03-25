.PHONY: setup test notebook all clean

setup:
	python -m pip install -r requirements.txt

test:
	python -m pytest tests/ -v

notebook:
	jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb --output analysis_executed.ipynb

all: setup test notebook

clean:
	rm -rf data/clean/*.csv
	rm -f notebooks/analysis_executed.ipynb
