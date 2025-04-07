"""Create a Pydatnic model that implements the contents of the files in xml.

The python code is generated statically so that the models can be inspected statically.
"""

import warnings
from xml.etree import ElementTree as ET

from wannier90_input.models import directory as model_directory
from wannier90_input.models.parameters import import_parameter_models
from wannier90_input.patches import allow_none as types_to_allow_none
from wannier90_input.patches import defaults as defaults_to_patch
from wannier90_input.patches import exclude as fields_to_exclide
from wannier90_input.patches import fields as fields_to_patch
from wannier90_input.patches import types as types_to_patch
from wannier90_input.xml_files import files as xml_files


def parse_type(xml_type: str):
    """Map XML type notation to Python types."""
    type_mapping = {
        'I': int,
        'R': float,
        'L': bool,
        'S': str,
        'P': float
    }
    return type_mapping.get(xml_type, str)


def generate_pydantic_model(xml_path: str, version: str = "latest") -> str:
    """Parse the XML file and generate a Pydantic model."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    class_definitions = {}

    fields = set([])
    for parameter in root.findall("parameter"):
        # For the moment, only implementing Wannier90 and not post-processing
        if parameter.attrib['tool'] != 'w90':
            continue
        name = parameter.find("name").text
        if name in fields_to_exclide:
            continue

        field_def = ""

        if name in fields_to_patch:
            field_def += fields_to_patch.pop(name)
        else:
            xml_type = parameter.find("type").text
            description = parameter.find("description").text
            choices = parameter.find("choices")
            default = parameter.find("default")

            if name in types_to_patch:
                type_str = types_to_patch[name]
            else:
                python_type = parse_type(xml_type)
                if choices:
                    type_str = "Literal[" + ", ".join(
                        [f"\"{c.text}\"" if python_type == str else python_type(c.text) for c in choices])
                    if name in types_to_allow_none:
                        type_str += ", None"
                    type_str += "]"
                else:
                    type_str = python_type.__name__

            if name in defaults_to_patch:
                value = defaults_to_patch[name]
                default_str = '"' + value + '"' if isinstance(value, str) else str(value)
            elif default is not None:
                assert default.text
                default_str = '"' + default.text + '"' if xml_type == "S" else default.text
            elif name in types_to_allow_none:
                default_str = "None"
                if not choices:
                    type_str += " | None"
            else:
                default_str = '...'
            field_def += f"{type_str} = Field({default_str}, description=\"{description}\")"

        if name in class_definitions:
            warnings.warn(f"Duplicate field name '{name}' in XML file. Ignoring new definition.")
        else:
            class_definitions[name] = field_def

        fields.add(name)

    class_definitions.update(**fields_to_patch)

    if version == "latest":
        version = ""

    return f"""from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Annotated, Literal
from numpydantic import NDArray, Shape
from wannier90_input.validators import before_validators, after_validators
from wannier90_input.models.utils import custom_str
{import_parameter_models}

class Wannier90Input{version}(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

""" + "\n".join([f"    {k}: {v}" for k, v in class_definitions.items()]) + "\n" + """
    @model_validator(mode='before')
    @classmethod
    def validate_before(cls, values):
        for validator in before_validators:
            values = validator(values)
        return values

    @model_validator(mode='after')
    @classmethod
    def validate_after(cls, values):
        for validator in after_validators:
            values = validator(cls, values)
        return values

    def __str__(self):
        return custom_str(self)
"""


def generate_models():
    for name, xml_file in xml_files.items():
        model_str = generate_pydantic_model(xml_file)

        model_filename = f"{name}.py"
        if name != "latest":
            # Avoid filenames that start with a number
            model_filename = "sha_" + model_filename
        with open(model_directory / model_filename, "w") as f:
            f.write(model_str)
        print("Model generated for", name)
