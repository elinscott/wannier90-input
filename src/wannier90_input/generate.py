"""Functions for converting XML files to python files that contain Pydantic models.

The python code is generated statically so that the models can be inspected statically.
"""

from pathlib import Path

from defusedxml.ElementTree import parse

from wannier90_input.convert import convert_xml_tree_to_model
from wannier90_input.models import directory as model_directory
from wannier90_input.xml_files import files as xml_files


def generate_model(xml_path: Path, version: str = "latest") -> None:
    """Parse the XML file and generate a Pydantic model."""
    tree = parse(xml_path)
    root = tree.getroot()

    try:
        model_str = convert_xml_tree_to_model(root, version=version)
    except ValueError as e:
        raise ValueError(f"Failed when parsing {xml_path!s}: {e}") from e

    model_filename = f"{version}.py"
    if version != "latest":
        # Avoid filenames that start with a number
        model_filename = "sha_" + model_filename
    with open(model_directory / model_filename, "w") as f:
        f.write(model_str)


def generate_models() -> None:
    """Generate Pydantic models from XML files."""
    for version, xml_file in xml_files.items():
        generate_model(xml_file, version)
