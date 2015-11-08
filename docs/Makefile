# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXAPIDOC  = sphinx-apidoc
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = build
CODESOURCE    = code/source
AGLIO		  = aglio

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

ifeq ($(shell which $(AGLIO) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(AGLIO)' command was not found. Make sure you have Aglio installed. If you don't have Aglio installed, grab it from https://github.com/danielgtaylor/aglio)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help clean html html-code latex changes linkcheck

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  html-code  to make standalone HTML files (with project code)"
	@echo "  changes    to make an overview of all changed/added/deprecated items"

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(CODESOURCE)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	#$(AGLIO) -i resources/v1.md -o $(BUILDDIR)/html/resources/v1.html
	$(AGLIO) -i resources/partner_v1.apib -o $(BUILDDIR)/html/resources/partner_v1.html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

html-code:
	$(SPHINXAPIDOC) -f -e -E -d 3 -o $(CODESOURCE)/api $(abspath ../api) migrations templatetags partner_v1/tests private_v1/tests
	$(SPHINXAPIDOC) -f -e -E -d 3 -o $(CODESOURCE)/data $(abspath ../data) migrations tests
	$(SPHINXAPIDOC) -f -e -E -d 3 -o $(CODESOURCE)/utils $(abspath ../utils)
	$(SPHINXAPIDOC) -f -e -E -d 3 -o $(CODESOURCE)/worker $(abspath ../worker)
	$(SPHINXBUILD) -b html -t code $(ALLSPHINXOPTS) $(BUILDDIR)/html-code
	#$(AGLIO) -i resources/v1.md -o $(BUILDDIR)/html-code/resources/v1.html
	$(AGLIO) -i resources/partner_v1.md -o $(BUILDDIR)/html-code/resources/partner_v1.html
	#$(AGLIO) -i resources/private_v1.md -o $(BUILDDIR)/html-code/resources/private_v1.html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html-code."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."
