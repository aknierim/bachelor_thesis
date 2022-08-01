#!/bin/bash
pwd := $$(pwd)
translate = $1

# colors / text formatting
BACKGR=`tput setaf 0`
RED=`tput setaf 1`
GREEN=`tput setaf 10`
GREENB=`tput setab 10`
BLUE=`tput setaf 4`
BOLD=`tput bold`
RESET=`tput sgr0`

TIKZFILES := $(wildcard tikz/*.tex) # list of all TikZ files
TIKZ_PDFS := $(subst tikz/,,$(TIKZFILES:.tex=)) # get names from TikZ files for .pdf output files


all: clean tikz build/thesis.pdf


TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

.DELETE_ON_ERROR:
build/thesis.pdf: FORCE | build
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) thesis.tex 1> build/log || cat build/log
	@mv build/thesis.pdf thesis.pdf
	@echo ${GREENB}${BACKGR}Success!${RESET}

tikz: FORCE tikz/ | build
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) $(TIKZFILES) 1> build/tikz_log || cat build/tikz_log
	@for name in $(TIKZ_PDFS) ; do \
		mv build/$$name.pdf graphics/$$name.pdf ; \
		rm build/$$name.aux build/$$name.fdb_latexmk build/$$name.fls build/$$name.log; \
	done


FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build

.PHONY: all clean
