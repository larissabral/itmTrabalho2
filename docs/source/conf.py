# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Simulador de Circuitos Elétricos"
copyright = "2025, Larissa Bral"
author = "Larissa Bral"
release = "0.1"

# -- Path setup --------------------------------------------------------------
# Adiciona a pasta src ao sys.path para que Sphinx encontre os módulos
sys.path.insert(0, os.path.abspath("../.."))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "pt_BR"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_rtd_theme"
