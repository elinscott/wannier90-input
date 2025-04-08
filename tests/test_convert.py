"""Testing the `wannier90_input.convert` module."""

import pytest
from defusedxml.ElementTree import parse
from xml.etree.ElementTree import Element
from pathlib import Path

from wannier90_input.convert import InvalidXMLStructureError, convert_xml_tree_to_model


@pytest.fixture
def example_xml(data_directory: Path) -> Element:
    """Return the filepath of an example XML file,"""
    xml = parse(data_directory / "valid.xml")
    assert isinstance(xml, Element)
    return xml

def test_convert_valid_xml(example_xml: Element) -> None:
    """Test converting valid XML."""
    convert_xml_tree_to_model(example_xml)

@pytest.mark.parametrize("missing_field", ["name", "type", "description"])
def test_convert_xml_missing_field(missing_field: str, example_xml: Element) -> None:
    """Test invalid XML that is missing a field."""
    # Remove the field "missing_field" from the valid xml
    field_removed = False
    for param in example_xml.findall("parameter"):
        element_to_remove = param.find(missing_field)
        if element_to_remove is not None:
            param.remove(element_to_remove)
            field_removed = True
            break
    assert field_removed

    # Try to parse the now-invalid XML; should exit gracefully
    with pytest.raises(InvalidXMLStructureError):
        convert_xml_tree_to_model(example_xml)
