# Minimal makefile for Sphinx documentation.
# This file defines targets and variables to simplify the process of building documentation with Sphinx.

# Variables:
# These can be set from the command line or environment to customize behavior.

SPHINXOPTS    ?=        # Additional options passed to the Sphinx build command. Can be set externally.
SPHINXBUILD   ?= sphinx-build  # Command to run the Sphinx build tool. Defaults to 'sphinx-build'.
SOURCEDIR     = source  # Directory containing the source files for the documentation.
BUILDDIR      = build   # Directory where the output (e.g., HTML, PDF) will be generated.

# Default target:
# The 'help' target provides information about available Sphinx build options.
# It runs when the "make" command is executed without arguments.
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# The @ suppresses command output in the terminal. This invokes Sphinx in "make mode" to show help.

# Declare targets that do not correspond to files as phony to avoid conflicts.
.PHONY: help Makefile

# Catch-all target:
# Routes any unknown target to Sphinx using its "make mode."
# The `$@` variable represents the name of the target invoked by the user.
# The `$(O)` variable is a shortcut for additional Sphinx options.
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# This allows users to invoke Sphinx build targets (e.g., "html", "pdf") directly using "make <target>".
