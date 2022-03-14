"""
Script to create the overall info files from
the various source files

"""

import json
import sqlite3
from pathlib import Path

import nbformat
import pandas as pd
from bs4 import BeautifulSoup
from htmltabletomd import convert_table
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import ExecutePreprocessor
from traitlets.config import Config


def remove_tables(body: str) -> str:
    """
    notebook is still outputing html tables
    conver to markdown

    """
    body = body.replace('<tr style="text-align: right;">\n      <th></th>', "<tr>")
    soup = BeautifulSoup(body, "html.parser")
    for div in soup.find_all("table"):
        table = convert_table(str(div))
        div.replaceWith(table)
    for div in soup.find_all("style"):
        div.replaceWith("")

    body = str(soup)
    body = body.replace("&lt;br/&gt;", "<br/>")
    body = body.replace("![png]", "![]")
    body = body.replace('<style type="text/css">', "")
    body = body.replace("</style>", "")
    body = body.replace("<div>", "")
    body = body.replace("</div>", "")
    while "\n\n\n" in body:
        body = body.replace("\n\n\n", "\n\n")

    return body


def render_readme():
    nb = nbformat.read(Path("notebooks", "service_descriptions.ipynb"), as_version=4)

    c = Config()
    # needs to reexecuite
    c.MarkdownExporter.exclude_input = True
    c.MarkdownExporter.exclude_input_prompt = True

    c.MarkdownExporter.preprocessors = [ExecutePreprocessor]

    exporter = MarkdownExporter(config=c)

    body, resources = exporter.from_notebook_node(nb, {})
    body = remove_tables(body)

    with open("readme.md", "w") as f:
        f.write(body)

if __name__ == "__main__":

    render_readme()
