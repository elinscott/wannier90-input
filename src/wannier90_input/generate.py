"""Create a Pydatnic model that implements the contents of the files in xml.

The python code is generated statically so that the models can be inspected statically.
"""

import warnings
from pathlib import Path
from xml.etree.ElementTree import Element

from defusedxml.ElementTree import parse

from wannier90_input.models import directory as model_directory
from wannier90_input.models.parameters import import_parameter_models
from wannier90_input.patches import allow_none as types_to_allow_none
from wannier90_input.patches import defaults as defaults_to_patch
from wannier90_input.patches import exclude as fields_to_exclude
from wannier90_input.patches import fields as fields_to_patch
from wannier90_input.patches import types as types_to_patch
from wannier90_input.xml_files import files as xml_files

type_mapping = {
    'I': int,
    'R': float,
    'L': bool,
    'S': str,
    'P': float
}


def convert_xml_tree_to_model(root: Element, version: str = "latest") -> str:

    class_definitions = {}

    fields = set()
    for parameter in root.findall("parameter"):
        name = _get_name(parameter)
        if name in fields_to_exclude:
            continue
        if name in class_definitions:
            warnings.warn(f"Duplicate field name '{name}' in XML file. Ignoring new definition.",
                          stacklevel=2)
            continue

        # For the moment, only implementing Wannier90 and not post-processing
        if parameter.attrib['tool'] != 'w90':
            continue

        field_def = _parse_parameter(parameter)

        if field_def is None:
            continue

        class_definitions[name] = field_def

        fields.add(name)

    class_definitions.update(**fields_to_patch)

    return _generate_model_string(class_definitions, version=version)

def _get_name(parameter: Element) -> str:
    name_element = parameter.find("name")
    if name_element is None:
        raise ValueError(f"`{parameter}` is missing the `name` field.")
    if name_element.text is None:
        raise ValueError(f"Failed to parse name element for `{parameter}`.")
    return name_element.text

def _parse_parameter(parameter: Element) -> str:
    name = _get_name(parameter)

    if name in fields_to_patch:
        return fields_to_patch.pop(name)
    else:
        type_element = parameter.find("type")
        if type_element is None:
            raise ValueError(f"`{parameter}` is missing the `type` field.")
        xml_type = type_element.text
        if xml_type is None:
            raise ValueError(f"Failed to parse type element for `{name}`.")

        description_element = parameter.find("description")
        if description_element is None:
            raise ValueError(
                f"`{parameter}` is missing the `description` field."
            )
        description = description_element.text

        choices = parameter.find("choices")
        default = parameter.find("default")

        type_str = _get_type_str(name, xml_type, choices)

        default_str = _get_default_str(name, xml_type, default, choices)

        if default_str == "None" and choices is None:
            type_str += " | None"

        return f"{type_str} = Field({default_str}, description=\"{description}\")"


def _get_type_str(name: str, xml_type: str, choices: Element | None) -> str:
    """Determine the string to add for the type of the field."""
    if name in types_to_patch:
        type_str = types_to_patch[name]
    else:
        python_type = type_mapping[xml_type]
        if choices:
            type_str = "Literal[" + ", ".join(
                [f"\"{c.text}\"" if python_type is str else python_type(c.text)
                 for c in choices])
            if name in types_to_allow_none:
                type_str += ", None"
            type_str += "]"
        else:
            type_str = python_type.__name__

    return type_str


def _get_default_str(name: str, xml_type: str, default: Element | None,
                     choices: Element | None) -> str:
    if name in defaults_to_patch:
        value = defaults_to_patch[name]
        default_str = '"' + value + '"' if isinstance(value, str) else str(value)
    elif default is not None:
        if default.text is None:
            raise ValueError(f"Missing text in XML file for `{name}`.")
        default_str = '"' + default.text + '"' if xml_type == "S" else default.text
    elif name in types_to_allow_none:
        default_str = "None"
    else:
        default_str = '...'
    return default_str


def _generate_model_string(class_definitions: dict[str, str], version: str) -> str:
    return '"""' + f"""Pydantic model for the input of `Wannier90` version `{version}`.

This file has been generated automatically. Do not edit it manually.
""" + '"""' + f"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from wannier90_input.models.template import Wannier90InputTemplate
{import_parameter_models}

class Wannier90Input(Wannier90InputTemplate):
    """ + '"""' + "Pydantic model for the input of `Wannier90.`" + '"""' + """

""" + "\n".join([f"    {k}: {v}" for k, v in class_definitions.items()]) + "\n"


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
