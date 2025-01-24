# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# Information about the project being documented.
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Open Science Toolkit Information Access'  # The name of the project.
copyright = '2024, Omar Briqa, Adrián Romera'  # Copyright information for the project.
author = 'Omar Briqa, Adrián Romera'  # Names of the authors.
release = '2.0'  # Release version of the project documentation.

# -- General configuration ---------------------------------------------------
# General settings for the Sphinx documentation builder.
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',  # Measures the duration of Sphinx builds.
    'sphinx.ext.doctest',  # Allows testing of code snippets in documentation.
    'sphinx.ext.autodoc',  # Automatically generates documentation from docstrings.
]

templates_path = ['_templates']  # Path to custom HTML templates.
exclude_patterns = []  # Patterns to exclude files/directories from the documentation build.

# -- Options for HTML output -------------------------------------------------
# Configuration for HTML output format.
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Specifies the HTML theme. 'sphinx_rtd_theme' is widely used.
