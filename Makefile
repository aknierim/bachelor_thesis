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


# plots
cosmic_flux=build/cosmic_flux.pgf
crab_ssc=build/crab_ssc.pdf
array_layout=build/array_layout.pgf


PLOTS := $(array_layout) #$(cosmic_flux) $(crab_ssc)


all: clean $(PLOTS) tikz build/thesis.pdf


TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

.DELETE_ON_ERROR:
build/thesis.pdf: FORCE | build
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) thesis.tex 1> build/log || cat build/log
	@mv build/thesis.pdf thesis.pdf
	@echo ${GREENB}${BACKGR}Success!${RESET}

# currently not working
lst: FORCE | build
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) "\def\lsttitle{1} \input{thesis.tex}" 1> build/log || cat build/log
	@echo ${GREENB}${BACKGR}Success!${RESET}

tikz: FORCE tikz/ | build
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) $(TIKZFILES) 1> build/tikz_log || cat build/tikz_log
	@for name in $(TIKZ_PDFS) ; do \
		mv build/$$name.pdf graphics/$$name.pdf ; \
		rm build/$$name.aux build/$$name.fdb_latexmk build/$$name.fls build/$$name.log; \
	done

$(cosmic_flux): plots/cosmic_flux.py matplotlibrc | build
	python plots/cosmic_flux.py

$(crab_ssc): plots/crab_ssc.py matplotlibrc | build
	python plots/crab_ssc.py

$(array_layout): plots/array_layout.py matplotlibrc | build
	python plots/array_layout.py

FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build

.PHONY: all clean