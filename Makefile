PY ?= python

.PHONY: all install extract excel charts report test clean

all: extract excel charts report

install:
	$(PY) -m pip install -e ".[dev]"

extract:  ## verify every ledger figure against the raw PDFs (OCR) and write data/processed/
	$(PY) -m rcfl extract

excel:    ## live-formula workbooks
	$(PY) -m rcfl excel

charts:
	$(PY) -m rcfl charts

report:   ## CSVs, docs/*.md and the two-page PDF
	$(PY) -m rcfl report

test:
	$(PY) -m pytest

clean:
	rm -rf data/interim data/processed outputs/*.xlsx outputs/*.csv outputs/*.pdf outputs/charts/*.png
