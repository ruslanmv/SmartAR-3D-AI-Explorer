# tests/test_ingestion.py

import os
import pytest
from app.modules.ingestion import ModelIngestion

@pytest.fixture
def ingestion_instance():
    """
    A pytest fixture that returns a fresh ModelIngestion instance 
    for each test.
    """
    return ModelIngestion()

def test_load_non_existing_file(ingestion_instance):
    """
    Ensure that loading a non-existing file doesn't crash,
    and returns a stub structure (e.g., {"geometry": None, "objects": []}).
    """
    fake_path = "non_existing_file.obj"
    result = ingestion_instance.load_model(fake_path)
    assert "geometry" in result
    assert "objects" in result
    assert result["geometry"] is None
    assert len(result["objects"]) == 0

def test_load_unsupported_extension(ingestion_instance, tmp_path):
    """
    If the file extension is unsupported, ingestion should return a stub 
    or log a message.
    """
    # Create a dummy file with an unsupported extension (e.g., .gltf)
    test_file = tmp_path / "dummy.gltf"
    test_file.write_text("mock data")  # Just to have a file present
    
    result = ingestion_instance.load_model(str(test_file))
    assert result["geometry"] is None
    assert len(result["objects"]) == 0

@pytest.mark.skipif(
    not hasattr(ingestion_instance.__class__, "_load_obj"), 
    reason="pywavefront or _load_obj might not be available"
)
def test_load_obj(ingestion_instance, tmp_path):
    """
    If pywavefront is installed and _load_obj is implemented,
    create a minimal .obj file and see if ingestion parses it 
    (even if partially).
    """
    # Minimal .obj file content (3 vertices forming 1 triangle)
    obj_content = """
    v 0.0 0.0 0.0
    v 1.0 0.0 0.0
    v 0.0 1.0 0.0
    f 1 2 3
    """
    test_file = tmp_path / "test_model.obj"
    test_file.write_text(obj_content.strip())

    result = ingestion_instance.load_model(str(test_file))
    assert result["format"] == "OBJ"
    # We expect something in geometry. We won't check specifics 
    # because each version of pywavefront might store them differently.
    assert "geometry" in result
    assert "objects" in result

@pytest.mark.skipif(
    not hasattr(ingestion_instance.__class__, "_load_ifc"), 
    reason="ifcopenshell or _load_ifc might not be available"
)
def test_load_ifc(ingestion_instance, tmp_path):
    """
    If ifcopenshell is installed and _load_ifc is implemented,
    test ingestion with a trivial IFC file.
    """
    # A minimal IFC file (exceedingly simplified). 
    # Real IFC examples are typically far more complex.
    # This might not parse fully, but let's see if ingestion can handle it.
    ifc_content = """
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('simple.ifc','2025-01-01T12:00:00',('Alice'),('SmartAR-3D-Robot-Explorer'),'+02','Test IFC','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPROJECT('1','MyProject',NULL,NULL,NULL,NULL,$,$);
ENDSEC;
END-ISO-10303-21;
    """.strip()

    test_file = tmp_path / "test_model.ifc"
    test_file.write_text(ifc_content)

    result = ingestion_instance.load_model(str(test_file))
    assert result["format"] == "IFC"
    # We expect geometry or objects structure 
    assert "geometry" in result
    assert "objects" in result
