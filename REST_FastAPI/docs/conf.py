import sys
import os

sys.path.append(os.path.abspath(".."))

project = "Contacts project"
copyright = "2024, SoloGen"
author = "SoloGen"

extensions = ["sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]
