from notebook_helper.management.cli import cli, set_doc_collection
from notebook_helper.management.render_processing import DocumentCollection
from pathlib import Path

if Path("render.yaml").exists():
    doc_collection = DocumentCollection.from_yaml("render.yaml")
    set_doc_collection(doc_collection)

# in principle using the click syntax you could hook further commands on the 'cli' group here.

if __name__ == "__main__":
    cli()
