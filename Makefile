# =============================================================================
#  Chem-151 — 2026 S.T. Yau High School Science Award (Asia)
#
#  make draft    build with placeholders visible          <- the working target
#  make check    run every check, report, do not fail
#  make final    build for submission; FAILS on any placeholder or bad DOI
#  make submit   produce admin/submission/Chem-151-Research Report.pdf
#
#  Deadline: 17 August 2026, 23:59 HKT = 21:29 IST. Target 16 August.
# =============================================================================

SHELL      := /bin/bash
ROOT       := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
PYENV      ?= /opt/homebrew/Caskroom/miniforge/base/envs/biosorb
PY         := $(PYENV)/bin/python
TEXBIN     ?= /Library/TeX/texbin
LATEXMK    := PATH="$(TEXBIN):$$PATH" latexmk
REPORT     := $(ROOT)/report
BUILD      := $(REPORT)/build
PDF        := $(BUILD)/main.pdf
SUBMISSION := $(ROOT)/admin/submission/Chem-151-Research Report.pdf

.DEFAULT_GOAL := help
.PHONY: help setup numbers figures tables draft final check submit log test clean distclean

# -----------------------------------------------------------------------------
help:
	@echo ""
	@echo "  Chem-151 build"
	@echo ""
	@echo "    make setup     create the biosorb environment and install git hooks"
	@echo "    make numbers   CANONICAL_NUMBERS.yaml -> report/preamble/numbers.tex"
	@echo "    make figures   figures/src/*.py       -> figures/out/"
	@echo "    make tables    tables/src/*.py        -> tables/out/"
	@echo "    make draft     build with placeholders visible"
	@echo "    make check     every check, reported; never fails the shell"
	@echo "    make final     submission build; FAILS on any placeholder or bad DOI"
	@echo "    make submit    copy to 'admin/submission/Chem-151-Research Report.pdf'"
	@echo "    make log       append this session to logs/ai_use_log.csv"
	@echo "    make test      run the analysis unit tests"
	@echo "    make clean     remove build artefacts"
	@echo ""

# -----------------------------------------------------------------------------
setup:
	@echo "==> python environment"
	@if [ ! -x "$(PY)" ]; then mamba env create -f environment.yml; else echo "    biosorb present"; fi
	@$(PY) -m ipykernel install --user --name biosorb --display-name biosorb >/dev/null 2>&1 || true
	@echo "==> git hooks"
	@bash scripts/install_hooks.sh
	@echo "==> toolchain"
	@source scripts/env.sh >/dev/null 2>&1; chem151_status 2>/dev/null || true

# -----------------------------------------------------------------------------
numbers:
	@$(PY) scripts/emit_numbers.py --draft

numbers-final:
	@$(PY) scripts/emit_numbers.py

figures:
	@if compgen -G "figures/src/*.py" > /dev/null; then \
	  for f in figures/src/*.py; do echo "==> $$f"; $(PY) "$$f" || exit 1; done; \
	else echo "    no figure scripts yet"; fi

tables:
	@if compgen -G "tables/src/*.py" > /dev/null; then \
	  for f in tables/src/*.py; do echo "==> $$f"; $(PY) "$$f" || exit 1; done; \
	else echo "    no table scripts yet"; fi

# -----------------------------------------------------------------------------
# DRAFT — placeholders render as loud coloured boxes. This is the working target.
draft: numbers
	@echo "==> latexmk (draft)"
	@cd $(REPORT) && $(LATEXMK) -interaction=nonstopmode main.tex
	@echo ""
	@echo "==> $(PDF)"
	@PATH="$(TEXBIN):$$PATH" pdfinfo "$(PDF)" | grep -E 'Pages|Page size'
	@if [ -f "$(BUILD)/main.placeholders" ]; then \
	  echo ""; echo "==> placeholders outstanding"; \
	  cut -d'|' -f1 "$(BUILD)/main.placeholders" | sort | uniq -c; fi

# -----------------------------------------------------------------------------
# CHECK — reports everything, fails nothing. Run this at the end of every session.
check:
	@echo "############ 1/5  placeholders ############"
	@-$(PY) scripts/check_placeholders.py
	@echo ""
	@echo "############ 2/5  numbers ############"
	@-$(PY) scripts/check_numbers.py
	@echo ""
	@echo "############ 3/5  references ############"
	@-$(PY) scripts/verify_dois.py
	@echo ""
	@echo "############ 4/5  data ############"
	@-$(PY) scripts/ingest.py
	@echo ""
	@echo "############ 5/5  compliance ############"
	@-$(PY) scripts/check_compliance.py

# -----------------------------------------------------------------------------
# FINAL — every gate is hard. Any placeholder, any unverified DOI, any compliance
# failure stops the build. There is no flag to skip a check.
final: numbers-final figures tables
	@echo "==> gate 1: no placeholders may remain"
	@$(PY) scripts/check_placeholders.py --strict
	@echo "==> gate 2: every DOI resolves and every work has been read"
	@$(PY) scripts/verify_dois.py --strict
	@echo "==> gate 3: build"
	@cd $(REPORT) && $(LATEXMK) -interaction=nonstopmode \
	    -usepretex='\finaltrue' -jobname=main main.tex
	@echo "==> gate 4: compliance against the built PDF"
	@$(PY) scripts/check_compliance.py --strict
	@echo ""
	@echo "FINAL BUILD PASSED ALL GATES."

submit: final
	@mkdir -p "$(ROOT)/admin/submission"
	@cp "$(PDF)" "$(SUBMISSION)"
	@echo "==> $(SUBMISSION)"
	@$(PY) scripts/check_compliance.py "$(SUBMISSION)"
	@SIZE=$$(du -m "$(SUBMISSION)" | cut -f1); \
	 if [ $$SIZE -gt 5 ]; then \
	   echo ""; echo "  $$SIZE MB EXCEEDS 5 MB — send a DOWNLOAD LINK, not an attachment (C-009)."; \
	 fi
	@echo ""
	@echo "  Submit ONE file to yauaward@ashk.org.hk before 17 Aug 2026 21:29 IST."

# -----------------------------------------------------------------------------
log:
	@echo "Usage: $(PY) scripts/log_session.py --tool ... --stage ... --purpose ..."
	@echo "         --output-use ... --verification ... --transcript ..."
	@$(PY) scripts/log_session.py --show 2>/dev/null || true

test:
	@$(PY) -m pytest analysis/tests -q

clean:
	@cd $(REPORT) && $(LATEXMK) -C >/dev/null 2>&1 || true
	@rm -rf $(BUILD)
	@echo "cleaned build artefacts"

distclean: clean
	@rm -f $(REPORT)/preamble/numbers.tex
	@rm -f $(REPORT)/main.placeholders
	@echo "cleaned generated files"
